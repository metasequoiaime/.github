# Security Policy

This is the organization-wide policy for Metasequoia IME (水杉输入法). It applies to every repository under `metasequoiaime` that does not carry its own `SECURITY.md`; where a repository has one, follow that file instead.

An input method sees everything the user types. Please treat defects that could expose composed text, learned user dictionaries, stored credentials, or API tokens as security issues, not ordinary bugs.

## Supported versions

| Component | Supported |
| --- | --- |
| MSIME-Windows | Latest published release |
| MSIME-Apple | Latest published release |
| MSIME-Linux | Latest published release |
| MSIME-Engine, MSIME-Docs, MSIME-Web | Current `main` |
| Archived repositories | Not supported; report against the successor repository |

Older releases do not receive backported fixes. Before reporting, confirm the problem still occurs on a current version.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability, and do not include sensitive proof-of-concept data in public discussions.

**Preferred: open a private security advisory.** Private vulnerability reporting is enabled on every active repository, so go to the affected repository's Security tab and choose "Report a vulnerability", or use the direct link — for example <https://github.com/metasequoiaime/MSIME-Windows/security/advisories/new>. This keeps the report encrypted end to end on GitHub, gives it a tracked thread, and lets a CVE be requested from the same place. Email cannot do any of that.

**Alternative: email.** If you cannot use GitHub, email `suzukaze.haduki@gmail.com` with the subject `Metasequoia IME security report`. Note that this is ordinary unencrypted email; do not send proof-of-concept material that would itself be sensitive if intercepted.

Either way, include:

- which repository and version or commit is affected;
- the operating system version and, on Windows, the host application involved;
- expected and observed behavior, with reproduction steps;
- the security or privacy impact you believe it has.

Attach only the minimum data needed to reproduce the issue. Never include real text typed with the input method, user dictionary contents, API keys, tokens, credentials, or signing material.

If you are unsure whether something counts as a security issue, report it privately first. An unnecessary private report costs far less than a public disclosure of a real one.

## Handling

This project is maintained by a very small number of people, so these are commitments we can actually keep rather than an aspirational SLA:

- **First response within 3 working days.** If you have not heard anything by then, the report did not reach us — please chase it through the other channel.
- **An assessment within 14 days**, saying whether it is accepted, what severity we think it is, and roughly when a fix will land.
- **Coordinated disclosure within 90 days.** If a fix is not released by then, you are free to publish. We would rather you disclose on schedule than hold a real issue indefinitely because we were slow.

Reporters are credited in the advisory and the release notes unless they ask not to be.

For ordinary defects and feature requests with no security or privacy impact, use the public issue tracker of the relevant repository.
