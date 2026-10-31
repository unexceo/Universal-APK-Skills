# Security and responsible use

## Intended use
Analysis and modification of APKs you own or are authorized to test, open-source apps, authorized research, education, and legitimate game modding. The instructions in this repository tell agents to refuse licensing/paywall bypass, anti-cheat evasion, credential theft, covert surveillance, malware creation or deployment, unauthorized access, and misuse of keys or tokens. These are instructions to AI agents, not technical enforcement; users remain responsible for lawful use.

## Handling samples
Analyze unknown or suspicious APKs statically. Never run them on your main device or host. Use an isolated emulator/VM with snapshots for any dynamic work. Do not upload third-party samples to services without the right to do so. Keep signing keys and keystore passwords out of chats and out of git (`.gitignore` excludes `*.keystore`/`*.jks`).

## Reporting a vulnerability in this repository
Report problems such as scripts that execute untrusted input, instructions that could cause an agent to leak secrets, or ways to bypass the safety rules, using GitHub private vulnerability reporting (Security tab → Report a vulnerability) or by contacting the maintainers privately. Do not open public issues for exploitable problems. Expect an acknowledgement within a reasonable time; this is a volunteer project without an SLA.

## Design notes
`apk_inventory.py` only reads ZIP metadata and 112 bytes of each DEX header; it extracts and executes nothing. Installer scripts only copy or link files from this repository.
