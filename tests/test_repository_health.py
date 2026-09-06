import copy
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from repository_health import workflow_problems, protection_problems, security_problems

NOW = datetime(2026, 9, 6, tzinfo=timezone.utc)


def run(number=1, age=1, conclusion='success', status='completed'):
    return dict(id=number, created_at=(NOW - timedelta(hours=age)).isoformat(),
                conclusion=conclusion, status=status)


class WorkflowHealth(unittest.TestCase):
    def setUp(self):
        self.workflow = dict(path='.github/workflows/ci.yml', state='active',
                             created_at=(NOW-timedelta(days=10)).isoformat())

    def test_idle_push_workflow_is_healthy(self):
        self.assertEqual(workflow_problems(self.workflow, [run(age=1000)], NOW), [])

    def test_disabled_missing_and_stuck_runs(self):
        for workflow, runs in [(dict(self.workflow, state='disabled_manually'), [run()]),
                               (self.workflow, []),
                               (self.workflow, [run(age=4, status='queued', conclusion=None)])]:
            self.assertTrue(workflow_problems(workflow, runs, NOW))

    def test_scheduled_workflow_needs_recent_success(self):
        self.assertEqual(workflow_problems(self.workflow, [run()], NOW, 48), [])
        self.assertTrue(workflow_problems(self.workflow, [run(age=49)], NOW, 48))
        self.assertTrue(workflow_problems(self.workflow, [run(conclusion='failure')], NOW, 48))
        self.assertTrue(workflow_problems(self.workflow, [run(status='in_progress', conclusion=None)], NOW, 48))

    def test_three_failures_ignore_superseded_cancellations(self):
        runs = [run(i, i, 'failure') for i in range(1, 4)]
        runs.insert(0, run(4, 0.5, 'cancelled'))
        self.assertTrue(workflow_problems(self.workflow, runs, NOW))
        self.assertEqual(workflow_problems(self.workflow, [run(5, 0.1)] + runs, NOW), [])
        self.assertEqual(workflow_problems(self.workflow, runs[1:3], NOW), [])

    def test_new_workflow_gets_bounded_setup_window(self):
        workflow = dict(self.workflow, created_at=(NOW-timedelta(hours=1)).isoformat())
        self.assertEqual(workflow_problems(workflow, [], NOW, 48), [])


class ProtectionHealth(unittest.TestCase):
    def setUp(self):
        self.policy = dict(checks=['Build'])
        self.rules = [dict(type=t) for t in ('deletion', 'non_fast_forward', 'pull_request')]
        self.rules.append(dict(type='required_status_checks', parameters=dict(
            required_status_checks=[dict(context='Build', integration_id=15368)])))

    def test_required_rules_and_checks(self):
        self.assertEqual(protection_problems(self.rules, self.policy), [])
        for index in range(len(self.rules)):
            self.assertTrue(protection_problems(self.rules[:index] + self.rules[index+1:], self.policy))
        wrong_app = copy.deepcopy(self.rules)
        wrong_app[-1]['parameters']['required_status_checks'][0]['integration_id'] = 42
        self.assertTrue(protection_problems(wrong_app, self.policy))

    def test_apple_fast_forward_exception_still_requires_checks(self):
        rules = [r for r in self.rules if r['type'] != 'pull_request']
        self.assertEqual(protection_problems(rules, dict(self.policy, require_pr=False)), [])
        self.assertTrue(protection_problems([], dict(self.policy, require_pr=False)))

    def test_security_configuration_drift_and_missing_permission(self):
        fields = ('dependabot_security_updates', 'secret_scanning', 'secret_scanning_push_protection')
        settings = dict(security_and_analysis={f: dict(status='enabled') for f in fields})
        config = dict(status='attached', configuration=dict(dependency_graph='enabled'))
        self.assertEqual(security_problems(settings, dict(enabled=True), config, True), [])
        self.assertTrue(security_problems({}, dict(enabled=True), config, True))
        self.assertTrue(security_problems(settings, dict(enabled=False), config, True))
        self.assertTrue(security_problems(settings, dict(enabled=True), {}, True))
        self.assertTrue(security_problems(settings, dict(enabled=True), config, False))


if __name__ == '__main__':
    unittest.main()
