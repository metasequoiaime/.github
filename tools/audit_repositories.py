"""Audit the versioned CI baseline in every maintained public organization repository."""
import argparse
import json
import subprocess
import sys
from urllib.parse import quote


def api(path, *arguments):
    result = subprocess.run(
        ['gh', 'api', '--method', 'GET', path, *arguments],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(f'{path}: {result.stderr.strip()}')
    return json.loads(result.stdout)


def audit(organization):
    repositories = api(f'orgs/{quote(organization, safe="")}/repos?per_page=100', '--paginate', '--slurp')
    failures = []
    count = 0
    for repository in (repo for page in repositories for repo in page):
        if repository['archived'] or repository['private']:
            continue
        count += 1
        name = repository['full_name']
        branch = repository['default_branch']
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
            print(f'{name}: inspected {len(paths)} workflow files on {branch}')
        except RuntimeError as error:
            failures.append(str(error))
    if not count:
        failures.append('No maintained public repositories returned; refusing an empty audit')
    for failure in failures:
        print(f'ERROR: {failure}', file=sys.stderr)
    print(f'Inspected {count} maintained public repositories; {len(failures)} problems')
    return bool(failures)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--organization', default='metasequoiaime')
    args = parser.parse_args()
    try:
        sys.exit(audit(args.organization))
    except (RuntimeError, json.JSONDecodeError) as error:
        sys.exit(str(error))
