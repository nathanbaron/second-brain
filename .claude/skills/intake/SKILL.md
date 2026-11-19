---
name: intake
description: Turn Nathan's captured conversations (TwinMind) into notes in the Notion Notes database and candidate tasks in Tasks, status To Process, across every facet of his life. Runs nightly on a schedule, and on demand whenever he asks — "run intake", "process this morning", "process the meeting with X", "catch me up on today", "what's in TwinMind". On demand it can cover just part of the day, including a capture still in progress. Nothing is promoted without him.
---

# Intake

TwinMind captures stretches of Nathan's day. This skill turns them into notes and candidate tasks in Notion. It never decides for him: every task lands as **To Process** and he triages it.

Before writing anything, read `standards/writing-notes.md` in this repository (in a Claude.ai upload it sits beside this file as `writing-notes.md`). It governs every word that reaches Notion. In short: notes read as minutes written by a person who was there. No mention of recordings, transcripts, TwinMind, Claude or AI. Reliability is stated in plain words.

## Two ways it runs

- **Nightly** (routine, about 22:45 Toronto): everything not yet processed, up to 72 hours back.
- **On demand** (Nathan asks in any Claude session): the scope he names, such as "this morning", "since lunch", "the 10:00 with Jason" or "everything so far today". With no scope given, process everything not yet processed today. A capture still in progress can be processed up to now; see *Watermark*.

Both use the same steps and the same log, so neither one duplicates the other.

## Where things live

| What | Where |
|---|---|
| Notes | `collection://817eb84f-6244-4a93-a337-af78078143cd` |
| Tasks | `collection://cd94ea0f-20a6-4575-b677-e7ab8a696918` |
| Areas (with Facet) | `collection://322fab77-4f41-42ea-a04e-159a0a057924` |
| People (work roster) | `collection://c9dfeada-c344-4e10-b006-54b61a777e5a` |
| Vessels and docks | `collection://1a1e3b69-de6d-8089-930b-000b44228d5e` |
| Speaker directory | `collection://9c5f3e0f-7d5b-4d90-ba38-3a493b3f50c1` |

Areas and facets:
- **Work:** Engineering Services (engineering, vessels, maintenance, scopes), Marine Management (people, organisation, operations).
- **Home and family:** Parenting, Marriage & Partnership, Home & Haven, Cooking, Financial Stewardship, Personal Admin.
- **Recovery and practice:** Recovery, Spiritual Practice (his own practice), Centre (management work for the Centre), Personal Growth.
- **The water:** Sailing & Seamanship, Swimming.
- **Self:** Health & Vitality, Creative Expression, Personal Systems, AI Partnership.

Each note or task gets one or two Areas. Only give it two when it genuinely belongs to both.

## The log: Source ID and the watermark

Every note carries a **Source ID** (a hidden text property): `<meeting_id> <HH:MM>-<HH:MM>`, the item and the local time span the note covers. Several notes from one capture share the meeting_id with different spans.

- **Processed spans.** Query Notes where `Source ID` is not empty. For each meeting_id, the latest end time is its **watermark**. Older notes may carry the key in `URL` instead, as `twinmind:summary-<meeting_id>`: treat those captures as fully processed.
- **What's left.** For each capture in scope, process only what comes after its watermark (`chunk.py --after HH:MM`). Captures with no notes start from the beginning.
- **In progress.** When a capture is still running, process up to the last clear break between conversations. Leave a conversation still under way for the next run. The note's span ends at that break, which becomes the new watermark.
- **Nothing in it.** A span with nothing worth a note still gets a one-line note, `Archived` checked, titled `YYYY-MM-DD — nothing to note (HH:MM–HH:MM)`, so the log accounts for all of it.

## Steps

1. **List.** Use `summary_search` with a date window (local time). For the newest material, including a capture still in progress, call it with no keywords; results come newest first. A capture with no summary yet may be missing from search: if Nathan names one, or the run expects one, fetch by ID. Large results are saved to a file; read them with `jq`. Work out what's left from the log.
2. **Triage from the summary.** Fetch the full text only when the span holds commitments, decisions or more than one conversation. A class or a dog walk usually needs only the summary.
3. **Chunk.** Save the fetched text to the scratchpad and run `python3 -I .claude/skills/intake/chunk.py <file> <outdir> --minutes 30 [--after HH:MM]`. Chunks are about 14 KB, cut at speaker changes with a short overlap. Read every chunk; don't skim.
4. **Split into conversations.** One note per real conversation, not per capture. A run of hallway exchanges on the same job is one conversation; a scheduled meeting is its own.
5. **Names the source gets wrong.** Procurement's Kerry (comes through as "Carrie"). Matt on the repair team is Matthew Arlt. Scott for compressors is Scott Steenburgh. "Feeney" is Robert Feeney, the new FHI manager, not a vessel. Steve on the terminal works is Steve Consitt. DPA is the Designated Person Ashore, a regulatory role (Dean's). The FRONTENAC II is run by Loyalist Township, and Robert (Bob) Woodman is their marine services supervisor. Vessels: WI3 = WOLFE ISLANDER III, AI2 = AMHERST ISLANDER II, and GLENORA comes through as "Nora" or "Gonora". Add to this list when he corrects one.
6. **Look up before linking.** Query open Tasks for duplicates by keyword and vessel; link through `Related Tasks` instead of duplicating. Resolve people in the People roster or the Speaker Directory, and link only when sure. Speakers come through as numbers, so who said what is inference: name someone only when the content makes it certain.
7. **Find related notes.** Search Notes for each conversation's main subject (vessel, person, project, topic) within the same facet. Set `Related notes` to at most three older notes that are genuinely about the same thing. A wrong link is worse than none.
8. **Write the notes** to the standard: title, 📝 icon, `AI summary`, `Source ID`, Areas, People, Vessel / Dock, Related notes; the body as the standard sets out.
9. **Write the tasks.** Status **To Process**, always. Areas, People, Ships and Docks, Notes (the note), Related Tasks. Leave Priority and dates empty unless a date was actually said. Body to the standard: **Background**, **Suggested handling**.
10. **Report.** See below. Then stop. Don't triage for him.

## Small and linked

His word, 16 Nov: the smaller the task, the more useful it is, and the value is in the web of links: task to note, task to task, task to vessel and person, note to note.
- Split a big item into small, doable tasks, and propose a Project for the parent.
- Link wherever the link is real. When unsure, name the candidate in the task body instead of setting the relation.

## What gets captured

Capture generously, because he reviews everything: his own commitments, things promised to him (suggested Waiting On), ideas he voiced as wants, and items whose owner is unclear (said so). Skip anything already done during the conversation, and anything that only concerns other people.

## What never goes in

- Anything `standards/writing-notes.md` excludes.
- Anything said in confidence, or that a manager asked to keep confidential. It stays out of Notion entirely and is named only in the report.
- From AA meetings and Centre classes: only what Nathan himself committed to.
- His feelings about how something landed on him. Those are for conversation, not notes.
- The MES Activity Log and the calendar. Not this skill's to write. If something looks like Activity Log or calendar material, say so in the task body and the report.

## The report

This is the one place to speak plainly about method and confidence.

- **On demand:** in chat. How many notes and tasks, with links. Anything time-sensitive. Anything kept out and why. Anything uncertain enough that he should check it.
- **Nightly:** the run's final message, in the same order, ending with one line: `Intake <date>: <n> notes, <n> tasks, <n> kept out, <failures or none>.`

## The count, for the briefing

The morning briefing carries one line: how many tasks are in To Process, how old the oldest is, and how many captures have no note.

```sql
SELECT COUNT(*) AS n, MIN("Created time") AS oldest
FROM "collection://cd94ea0f-20a6-4575-b677-e7ab8a696918"
WHERE "Status" = 'To Process' AND ("Archived" IS NULL OR "Archived" = '__NO__')
```

Flag it when the oldest is more than three days old or the count is over 25.
