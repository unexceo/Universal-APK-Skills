# Generic / chat-only adapter

Use for platforms that cannot install repositories: ChatGPT (custom GPT or Project), Gemini Gems, Claude Projects, any chat UI.

1. Paste `UNIVERSAL_PROMPT.md` as the instructions (it is about 5 KB, so it should fit the 8,000-character custom-GPT instruction limit known at the time of writing; check the current limit).
2. Optional but better: attach `AGENTS.md` and the `skills/*/SKILL.md` files as knowledge/project files so the model can read full workflows.
3. Say "Install this repository", or type `/helpapk`.

Limits: instructions are active only inside that GPT/Gem/Project or conversation; commands are typed text, not registered slash commands; no local tools, so the assistant works in guidance mode (you run commands, paste output). If code execution is enabled in your product, the analysis inventory script (`skills/analyzeapk/scripts/apk_inventory.py`) can run on an uploaded APK; Android tools such as apktool and adb are normally unavailable in those sandboxes.
