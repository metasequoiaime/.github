"""Audit the versioned CI baseline in every maintained public organization repository."""
import argparse
import base64
import json
import subprocess
import sys
from pathlib import Path
from product_locks import ENGINE_SUBMODULE_PATH, PLATFORM_REPOSITORIES, audit_product_locks
from repository_health import audit_repository, organization_problems
from urllib.parse import quote


def api(path, *arguments):
    result = subprocess.run(
        ['gh', 'api', '--method', 'GET', path, *arguments],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(f'{path}: {result.stderr.strip()}')
    return json.loads(result.stdout) if result.stdout.strip() else None


def contents(repository, path):
    """Return the decoded file at `path`, or None when the repository does not carry it."""
    try:
        entry = api(f'repos/{repository}/contents/{path}')
    except RuntimeError:
        return None
    return base64.b64decode(entry['content']) if entry.get('type') == 'file' else None


def gitlink(repository, path):
    """Return the commit a submodule points at, or None when the path is absent."""
    try:
        entry = api(f'repos/{repository}/contents/{path}')
    except RuntimeError:
        return None
    return entry['sha'] if entry.get('type') == 'submodule' else None


def product_lock_findings(organization):
    locks, pins = {}, {}
    for name in PLATFORM_REPOSITORIES:
        repository = f'{organization}/{name}'
        raw = contents(repository, 'product-lock.json')
        if raw is None:
            return [f'{name}: product-lock.json is unreadable'], []
        locks[name] = json.loads(raw)
        pins[name] = gitlink(repository, ENGINE_SUBMODULE_PATH)
    engine = api(f'repos/{organization}/MSIME-Engine/commits?per_page=100', '--paginate', '--slurp')
    history = [commit['sha'] for page in engine for commit in page]
    return audit_product_locks(locks, pins, history)


def audit(organization, health=False, report=None):
    repositories = api(f'orgs/{quote(organization, safe="")}/repos?per_page=100', '--paginate', '--slurp')
    policies = json.loads(Path(__file__).with_name("health-policy.json").read_text())
    failures = []
    results = []
    count = 0
    for repository in (repo for page in repositories for repo in page):
        if repository['archived'] or repository['private']:
            continue
        count += 1
        name = repository['full_name']
        branch = repository['default_branch']
        start = len(failures)
        try:
            files = api(f'repos/{name}/contents/.github', '-f', f'ref={branch}')
            names = {item['name'] for item in files if item['type'] == 'file'}
            if not names.intersection({'dependabot.yml', 'dependabot.yaml'}):
                failures.append(f'{name}: missing .github/dependabot.yml')
            workflows = api(f'repos/{name}/contents/.github/workflows', '-f', f'ref={branch}')
            paths = {item['name'] for item in workflows if item['type'] == 'file'}
            for required in ('quality.yml', 'codeql.yml'):
                if required not in paths:
                    failures.append(f'{name}: missing .github/workflows/{required}')
            if not paths.intersection({'ci.yml', 'docs.yml'}):
                failures.append(f'{name}: missing functional CI or documentation validation')
            enabled = api(f'repos/{name}/actions/workflows?per_page=100')['workflows']
            for workflow in enabled:
                if workflow['path'] in {f'.github/workflows/{p}' for p in paths} and workflow['state'] != 'active':
                    failures.append(f'{name}: {workflow["path"]} is {workflow["state"]}')
            if health:
                failures.extend(f'{name}: {problem}' for problem in audit_repository(repository, api, policies.get(repository['name'])))
            print(f'{name}: inspected {len(paths)} workflow files on {branch}')
        except (RuntimeError, KeyError, ValueError, TypeError) as error:
            failures.append(f'{name}: {error}')
        results.append({"repository": name, "problems": failures[start:]})
    if not count:
        failures.append('No maintained public repositories returned; refusing an empty audit')

    notes = []
    try:
        lock_problems, notes = product_lock_findings(organization)
        failures.extend(lock_problems)
    except (RuntimeError, KeyError, ValueError, TypeError) as error:
        failures.append(f'product locks: {error}')
    if health:
        try:
            failures.extend(organization_problems(api(f'orgs/{quote(organization, safe="")}')))
        except (RuntimeError, KeyError, ValueError, TypeError) as error:
            failures.append(f'organization settings: {error}')
    for note in notes:
        print(f'NOTE: {note}')

    if report:
        Path(report).write_text(json.dumps(
            {'repositories': results, 'problems': failures, 'notes': notes}, indent=2) + '\n')
    for failure in failures:
        print(f'ERROR: {failure}', file=sys.stderr)
    print(f'Inspected {count} maintained public repositories; {len(failures)} problems')
    return bool(failures)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--organization', default='metasequoiaime')
    parser.add_argument('--health', action='store_true', help='Also inspect live runs and security/protection settings')
    parser.add_argument('--report', help='Write a machine-readable health report')
    args = parser.parse_args()
    try:
        sys.exit(audit(args.organization, args.health, args.report))
    except (RuntimeError, json.JSONDecodeError) as error:
        sys.exit(str(error))
