import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from product_locks import audit_product_locks, dictionary_problems, engine_pin_report, normalize_lock

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


def artifact(name, digest, url):
    return dict(name=name, sha256=digest, size=1, url=url)


RELEASE = 'https://github.com/metasequoiaime/msime-engine/releases/download/dict-v1.0.0/'


class LockFormats(unittest.TestCase):
    def test_artifact_lock_takes_the_dictionary_release_and_ignores_other_assets(self):
        lock = dict(source_commit='d0dc0c2', artifacts=[
            artifact('msime.db', 'aa', RELEASE + 'msime.db'),
            artifact('sentence-model.safetensors', 'mm',
                     'https://github.com/metasequoiaime/chinese-ime-lm/releases/download/model-v1/sentence-model.safetensors'),
        ])
        self.assertEqual(normalize_lock(lock), {'dictionary': dict(
            repository='metasequoiaime/msime-engine', tag='dict-v1.0.0', source_commit='d0dc0c2', assets={'msime.db': 'aa'})})

    def test_both_formats_agree_when_they_pin_the_same_release(self):
        artifacts = dict(source_commit='d0dc0c2', artifacts=[artifact('msime.db', 'aa', RELEASE + 'msime.db')])
        locks = {'msime-windows': normalize_lock(lock(**{'msime.db': 'aa'})), 'msime': normalize_lock(artifacts)}
        # MSIME-Engine and msime-engine are the same repository; case alone is not a mismatch.
        self.assertEqual(dictionary_problems(locks), [])

    def test_artifact_lock_spanning_two_dictionary_releases_is_rejected(self):
        lock = dict(source_commit='d0dc0c2', artifacts=[
            artifact('msime.db', 'aa', RELEASE + 'msime.db'),
            artifact('english.db', 'bb', RELEASE.replace('dict-v1.0.0', 'dict-v2.0.0') + 'english.db'),
        ])
        with self.assertRaises(ValueError):
            normalize_lock(lock)


class CombinedAudit(unittest.TestCase):
    def test_without_engine_pins_only_dictionary_problems_are_reported(self):
        locks = {'msime-windows': lock(**{'msime.db': 'aa'}), 'msime': lock(**{'msime.db': 'cc'})}
        problems, notes = audit_product_locks(locks)
        self.assertTrue(any('msime.db' in problem for problem in problems))
        self.assertEqual(notes, [])

    def test_problems_and_notes_are_kept_apart(self):
        locks = {'MSIME-Windows': lock(**{'msime.db': 'aa'}), 'MSIME-Apple': lock(**{'msime.db': 'cc'})}
        pins = {'MSIME-Windows': 'c00', 'MSIME-Apple': 'c03'}
        problems, notes = audit_product_locks(locks, pins, HISTORY)
        self.assertTrue(any('msime.db' in problem for problem in problems))
        self.assertEqual(len(notes), 1)


if __name__ == '__main__':
    unittest.main()
