"""Read-only checks for workflow health and repository protection drift."""
from datetime import datetime, timezone, timedelta

BAD = {'failure', 'timed_out', 'action_required', 'startup_failure', 'stale'}


def timestamp(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))


def workflow_problems(workflow, runs, now, max_age_hours=None):
    problems = []
    name = workflow['path']
    if workflow['state'] != 'active':
        problems.append(f'{name}: workflow is {workflow["state"]}')
    runs = sorted(runs, key=lambda r: r['created_at'], reverse=True)
    if not runs:
        if now - timestamp(workflow['created_at']) > timedelta(hours=24):
            problems.append(f'{name}: no default-branch runs after the 24-hour setup window')
        return problems
    if max_age_hours and now - timestamp(runs[0]['created_at']) > timedelta(hours=max_age_hours):
        problems.append(f'{name}: no run in the last {max_age_hours} hours')
    for run in runs:
        if run['status'] != 'completed' and now - timestamp(run['created_at']) > timedelta(hours=3):
            problems.append(f'{name}: run {run["id"]} has been queued/running for more than 3 hours')
    completed = [r for r in runs if r['status'] == 'completed' and r['conclusion'] != 'cancelled']
    if len(completed) >= 3 and all(r['conclusion'] in BAD for r in completed[:3]):
        problems.append(f'{name}: last three completed runs failed ({", ".join(str(r["id"]) for r in completed[:3])})')
    if max_age_hours:
        success = next((r for r in completed if r['conclusion'] == 'success'), None)
        if success is None or now - timestamp(success['created_at']) > timedelta(hours=max_age_hours):
            problems.append(f'{name}: no successful run within {max_age_hours} hours')
    return problems


def protection_problems(rules, policy):
    problems = []
    types = {r['type'] for r in rules}
    expected_types = {'deletion', 'non_fast_forward', 'required_status_checks'}
    if policy.get('require_pr', True):
        expected_types.add('pull_request')
    for kind in sorted(expected_types - types):
        problems.append(f'main protection: missing {kind}')
    checks = {c['context']: c.get('integration_id')
              for r in rules if r['type'] == 'required_status_checks'
              for c in r['parameters']['required_status_checks']}
    for context in policy['checks']:
        if context not in checks:
            problems.append(f'main protection: missing required check {context}')
        elif checks[context] != 15368:
            problems.append(f'main protection: {context} is not pinned to GitHub Actions')
    return problems


def security_problems(settings, private_reporting, configuration, alerts_enabled):
    problems = []
    for field in ('dependabot_security_updates', 'secret_scanning', 'secret_scanning_push_protection'):
        if settings.get('security_and_analysis', {}).get(field, {}).get('status') != 'enabled':
            problems.append(f'security: {field} disabled or unreadable with the audit credential')
    if not private_reporting.get('enabled'):
        problems.append('security: private vulnerability reporting disabled')
    if not alerts_enabled:
        problems.append('security: Dependabot alerts disabled')
    if configuration.get('status') != 'attached' or configuration.get('configuration', {}).get('dependency_graph') != 'enabled':
        problems.append('security: enabled dependency graph configuration is not attached')
    return problems


# Repository settings are audited above, but the organization settings that decide who may create,
# delete or expose a repository are not versioned anywhere and drift silently. Every member currently
# has 2FA on by choice; requiring it at the organization level is what keeps that true for the next
# member and for outside collaborators.
ORGANIZATION_EXPECTATIONS = {
    'two_factor_requirement_enabled': True,
    'members_can_delete_repositories': False,
    'members_can_change_repo_visibility': False,
    'members_can_create_public_repositories': False,
    'members_can_create_private_repositories': False,
    'dependabot_alerts_enabled_for_new_repositories': True,
    'dependabot_security_updates_enabled_for_new_repositories': True,
    'dependency_graph_enabled_for_new_repositories': True,
    'secret_scanning_enabled_for_new_repositories': True,
    'secret_scanning_push_protection_enabled_for_new_repositories': True,
}


def organization_problems(settings, expectations=None):
    problems = []
    for field, expected in (expectations or ORGANIZATION_EXPECTATIONS).items():
        if field not in settings:
            problems.append(f'organization: {field} unreadable with the audit credential')
        elif settings[field] is not expected:
            problems.append(f'organization: {field} is {settings[field]!r}, expected {expected!r}')
    if 'default_repository_permission' not in settings:
        problems.append('organization: default_repository_permission unreadable with the audit credential')
    elif settings['default_repository_permission'] not in ('read', 'none'):
        permission = settings['default_repository_permission']
        problems.append(f'organization: default_repository_permission is {permission!r}, expected read or none')
    return problems


def audit_repository(repository, api, policy, now=None):
    now = now or datetime.now(timezone.utc)
    prefix = 'repos/' + repository['full_name']
    branch = repository['default_branch']
    problems = []
    if policy is None:
        return ['No health policy for this maintained repository; review its required checks and release path']
    rules = api(f'{prefix}/rules/branches/{branch}')
    problems.extend(protection_problems(rules, policy))
    settings = api(prefix)
    reporting = api(f'{prefix}/private-vulnerability-reporting')
    configuration = api(f'{prefix}/code-security-configuration')
    # This endpoint is 204 when enabled and 404 when disabled. A denied request is an audit failure.
    api(f'{prefix}/vulnerability-alerts')
    problems.extend(security_problems(settings, reporting, configuration, True))
    workflows = api(f'{prefix}/actions/workflows?per_page=100')['workflows']
    by_path = {w['path'].removeprefix('.github/workflows/'): w for w in workflows}
    for path, cadence in policy['workflows'].items():
        workflow = by_path.get(path)
        if workflow is None:
            problems.append(f'{path}: missing registered workflow')
            continue
        runs = api(f'{prefix}/actions/workflows/{workflow["id"]}/runs?branch={branch}&per_page=100')['workflow_runs']
        runs = [r for r in runs if r['event'] in ('push', 'schedule', 'workflow_dispatch', 'repository_dispatch')]
        problems.extend(workflow_problems(workflow, runs, now, cadence))
    return problems
