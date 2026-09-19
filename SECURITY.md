# Security

CogC processes agent context and may therefore receive secrets or sensitive business data.

- Do not log raw source material by default in production integrations.
- Keep authorization and security constraints at C0.
- Treat third-party compression backends as data processors and review their data flow before enabling them.
- Do not send protected context to external inference providers merely to compress it unless the surrounding system explicitly authorizes that transfer.
- Report security issues privately to the repository maintainer once a maintainer address is configured.
