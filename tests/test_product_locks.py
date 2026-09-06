import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from product_locks import audit_product_locks, dictionary_problems, engine_pin_report

TAG = dict(repository='metasequoiaime/MSIME-Engine', tag='dict-v1.0.0', source_commit='d0dc0c2')
HISTORY = ['c%02d' % index for index in range(30)]


def lock(**assets):
    return dict(schema_version=1, dictionary=dict(TAG, assets=assets))


class DictionaryLocks(unittest.TestCase):
    def setUp(self):
        self.locks = {
            'MSIME-Windows': lock(**{'msime.db': 'aa', 'dict_japanese.dat': 'bb'}),
            'MSIME-Linux': lock(**{'msime.db': 'aa', 'dict_japanese.dat': 'bb'}),
            # Apple ships a subset; carrying fewer assets is not a mismatch.
            'MSIME-Apple': lock(**{'msime.db': 'aa'}),
        }

    def test_matching_locks_and_partial_asset_sets_are_clean(self):
        self.assertEqual(dictionary_problems(self.locks), [])

    def test_shared_asset_with_a_different_digest_fails(self):
        locks = copy.deepcopy(self.locks)
        locks['MSIME-Apple']['dictionary']['assets']['msime.db'] = 'cc'
        problems = dictionary_problems(locks)
        self.assertEqual(len(problems), 1)
        self.assertIn('msime.db', problems[0])

    def test_tag_and_source_commit_must_agree(self):
        for field, value in (('tag', 'dict-v1.1.0'), ('source_commit', 'ffffff'), ('repository', 'x/y')):
            locks = copy.deepcopy(self.locks)
            locks['MSIME-Linux']['dictionary'][field] = value
            self.assertTrue(any(field in problem for problem in dictionary_problems(locks)))

    def test_missing_dictionary_section_is_reported(self):
        locks = dict(self.locks, **{'MSIME-Apple': dict(schema_version=1)})
        self.assertTrue(any('no dictionary section' in problem for problem in dictionary_problems(locks)))

    def test_a_single_lock_cannot_disagree_with_anything(self):
        self.assertEqual(dictionary_problems({'MSIME-Apple': self.locks['MSIME-Apple']}), [])


class EnginePins(unittest.TestCase):
    def test_identical_pins_produce_neither_problem_nor_note(self):
        pins = dict.fromkeys(('MSIME-Windows', 'MSIME-Apple', 'MSIME-Linux'), 'c05')
        self.assertEqual(engine_pin_report(pins, HISTORY), ([], []))

    def test_diverging_pins_are_a_note_not_a_failure(self):
        pins = {'MSIME-Windows': 'c00', 'MSIME-Apple': 'c07', 'MSIME-Linux': 'c07'}
        problems, notes = engine_pin_report(pins, HISTORY)
        self.assertEqual(problems, [])
        self.assertEqual(len(notes), 1)
        self.assertIn('0 commits behind', notes[0])
        self.assertIn('7 commits behind', notes[0])

    def test_pin_outside_the_default_branch_fails(self):
        pins = {'MSIME-Windows': 'deadbeef', 'MSIME-Apple': 'c00', 'MSIME-Linux': 'c00'}
        problems, _ = engine_pin_report(pins, HISTORY)
        self.assertEqual(len(problems), 1)
        self.assertIn('not on the engine default branch', problems[0])

    def test_missing_gitlink_fails(self):
        problems, _ = engine_pin_report({'MSIME-Apple': None}, HISTORY)
        self.assertTrue(problems)


class CombinedAudit(unittest.TestCase):
    def test_problems_and_notes_are_kept_apart(self):
        locks = {'MSIME-Windows': lock(**{'msime.db': 'aa'}), 'MSIME-Apple': lock(**{'msime.db': 'cc'})}
        pins = {'MSIME-Windows': 'c00', 'MSIME-Apple': 'c03'}
        problems, notes = audit_product_locks(locks, pins, HISTORY)
        self.assertTrue(any('msime.db' in problem for problem in problems))
        self.assertEqual(len(notes), 1)


if __name__ == '__main__':
    unittest.main()
