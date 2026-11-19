# Nightly Intake: routine prompt

Paste everything below the line into the routine's prompt on claude.ai.

Settings: schedule `CRON_TZ=America/Toronto 45 22 * * *`. Connectors: Notion, TwinMind. Environment: Elysia Virelle. Permission mode: auto. Push notification on.

Revised 2026-11-19 after the first run: routine sessions have no add_repo tool, so the prompt falls back to a direct clone. Revised again 2026-11-19: intake now proposes MES Activity Log entries for approval (step 4).

---

Run tonight's intake for Nathan Baron.

1. Get the repository nathanbaron/second-brain. If an add_repo tool is available (load it with ToolSearch if it is deferred), attach it with read access and clone it as that tool instructs. If there is no add_repo tool, clone directly: `git clone --depth 1 https://github.com/nathanbaron/second-brain`. Either way, work from the repository's top folder.
2. Read standards/writing-notes.md, then follow .claude/skills/intake/SKILL.md in that repository exactly, in nightly mode: everything not yet processed, up to 72 hours back.
3. Use Toronto time throughout (TZ=America/Toronto date).
4. Write only to the Notion Notes and Tasks databases, and to the MES Activity Log only as the skill's *Activity Log proposals* section allows (proposed entries, proposed update lines, and promoting approved entries). Commit nothing. Never write to the calendar or any other page.
5. If TwinMind or Notion can't be reached, stop and say so; write nothing partial.

End with the report the skill describes, finishing with its one-line summary.
