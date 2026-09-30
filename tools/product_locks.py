"""Cross-repository consistency checks for the product lock files.

Each platform repository pins the shared dictionary release in its own lock file: msime-windows in `product-lock.json`, the msime monorepo in `resources/desktop-dictionary.lock.json`, and the two use different formats. Every repository validates its own lock, but nothing else compares them, so the products can quietly ship different data under the same dictionary tag.

The engine used to be a separate repository pinned by submodule gitlink; it now lives inside each product repository, so the engine pin comparison below is no longer wired into the audit.

Checks return `(problems, notes)`. Problems fail the audit. Notes are reported and do not: platforms bump the engine at different times, so a pin difference is normal and only worth showing.
"""
from urllib.parse import urlparse

# Platform repository -> path of the lock that pins its dictionary release.
PLATFORM_LOCKS = {
    'msime-windows': 'product-lock.json',
    'msime': 'resources/desktop-dictionary.lock.json',
}
ENGINE_SUBMODULE_PATH = 'vendor/MetasequoiaImeEngine'


def normalize_lock(lock):
    """Return `lock` in the product-lock.json shape, `{'dictionary': {repository, tag, source_commit, assets}}`.

    The msime lock lists download artifacts instead. Only artifacts from a `dict-*` release belong to the dictionary; the same list also carries models from other repositories. GitHub does not guarantee the case of a repository name in a URL, so the repository is compared in lower case.
    """
    if 'artifacts' not in lock:
        dictionary = lock.get('dictionary')
        if dictionary:
            lock = dict(lock, dictionary=dict(dictionary, repository=dictionary.get('repository', '').lower()))
        return lock
    releases, assets = set(), {}
    for artifact in lock['artifacts']:
        parts = urlparse(artifact['url']).path.strip('/').split('/')
        # owner/repository/releases/download/<tag>/<name>
        if len(parts) == 6 and parts[2:4] == ['releases', 'download'] and parts[4].startswith('dict-'):
            releases.add((f'{parts[0]}/{parts[1]}'.lower(), parts[4]))
            assets[artifact['name']] = artifact['sha256']
    if len(releases) != 1:
        raise ValueError(f'lock must reference exactly one dictionary release, found {sorted(releases)}')
    (repository, tag), = releases
    return {'dictionary': {'repository': repository, 'tag': tag, 'source_commit': lock.get('source_commit'), 'assets': assets}}


def dictionary_problems(locks):
    """Compare the dictionary section of every platform lock. `locks` maps repository name to lock."""
    problems = []
    present = {name: lock.get('dictionary') for name, lock in locks.items() if lock.get('dictionary')}
    for name in sorted(set(locks) - set(present)):
        problems.append(f'{name}: product-lock.json has no dictionary section')
    if len(present) < 2:
        return problems

    for field in ('repository', 'tag', 'source_commit'):
        values = {name: dictionary.get(field) for name, dictionary in present.items()}
        if len(set(values.values())) > 1:
            detail = ', '.join(f'{name}={values[name]!r}' for name in sorted(values))
            problems.append(f'dictionary {field} differs across platforms: {detail}')

    # Platforms legitimately ship different subsets of the release -- Apple does not carry the Japanese
    # data. What they must never disagree on is the digest of an asset they both carry, because that
    # means one of them is shipping something other than the tagged release.
    digests = {}
    for name, dictionary in sorted(present.items()):
        for asset, digest in sorted(dictionary.get('assets', {}).items()):
            digests.setdefault(asset, {})[name] = digest
    for asset, by_repository in sorted(digests.items()):
        if len(set(by_repository.values())) > 1:
            detail = ', '.join(f'{name}={by_repository[name][:12]}' for name in sorted(by_repository))
            problems.append(f'dictionary asset {asset} has different digests: {detail}')
    return problems


def engine_pin_report(pins, engine_history):
    """`pins` maps repository name to the engine gitlink; `engine_history` lists engine default-branch
    commits, newest first. A pin that is not on that list points at a commit the engine has not
    published, which is a problem; pins that merely differ from each other are a note."""
    problems, notes = [], []
    position = {commit: index for index, commit in enumerate(engine_history)}
    for name in sorted(pins):
        if pins[name] is None:
            problems.append(f'{name}: no {ENGINE_SUBMODULE_PATH} gitlink')
        elif pins[name] not in position:
            problems.append(f'{name}: engine pin {pins[name][:12]} is not on the engine default branch')
    known = {name: position[pin] for name, pin in pins.items() if pin in position}
    if len(set(known.values())) > 1:
        detail = ', '.join(f'{name}={pins[name][:12]} ({known[name]} commits behind engine main)'
                           for name in sorted(known, key=lambda n: known[n]))
        notes.append(f'engine pins differ across platforms: {detail}')
    return problems, notes


def audit_product_locks(locks, pins=None, engine_history=None):
    if pins is None:
        return dictionary_problems(locks), []
    problems, notes = engine_pin_report(pins, engine_history)
    return dictionary_problems(locks) + problems, notes
