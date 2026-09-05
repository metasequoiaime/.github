# Security Policy

This is the organization-wide policy for Metasequoia IME (水杉输入法). It applies to every repository under `metasequoiaime` that does not carry its own `SECURITY.md`; where a repository has one, follow that file instead.

An input method sees everything the user types. Please treat defects that could expose composed text, learned user dictionaries, stored credentials, or API tokens as security issues, not ordinary bugs.

## Supported versions

Security fixes are provided for the latest published release of each platform frontend, and for the current `main` of repositories that do not publish releases. Before reporting, confirm the problem still occurs on a current version.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability, and do not include sensitive proof-of-concept data in public discussions.

Email `suzukaze.haduki@gmail.com` with the subject `Metasequoia IME security report`. Include:

- which repository and version or commit is affected;
- the operating system version and, on Windows, the host application involved;
- expected and observed behavior, with reproduction steps;
- the security or privacy impact you believe it has.

Attach only the minimum data needed to reproduce the issue. Never include real text typed with the input method, user dictionary contents, API keys, tokens, credentials, or signing material.

If you are unsure whether something counts as a security issue, report it privately first. An unnecessary private report costs far less than a public disclosure of a real one.

## Handling

The maintainer will coordinate disclosure and remediation with the reporter. Please allow time for a fixed release to become available before publishing technical details.

For ordinary defects and feature requests with no security or privacy impact, use the public issue tracker of the relevant repository.
