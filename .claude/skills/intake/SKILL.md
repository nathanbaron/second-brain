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
6. **Look up before linking.** Resolve every named person in the People roster or the Speaker Directory. Speakers come through as numbers, so who *said* something is inference; but when a name is plainly used ("send it to Tyrone", "Rob's ordering the sensors") and matches one roster entry, link it. Leave it unlinked only when the name is ambiguous (two Jasons, three Robs) or the person isn't in the roster, and then name them in the body.
7. **Cross-check every commitment against Tasks.** See *The cross-check* below. Do this before writing a single task.
8. **Find related notes.** Search Notes for each conversation's main subject (vessel, person, project, topic) within the same facet. Set `Related notes` to at most three older notes that are genuinely about the same thing. A wrong link is worse than none.
9. **Write the notes** to the standard: title, 📝 icon, `AI summary`, `Source ID`, Areas, People, Vessel / Dock, Related notes; the body as the standard sets out.
10. **Write the tasks**, with the properties filled, not just the body. See *Task properties* below. Status **To Process**, always. Body to the standard: **Background**, **Suggested handling**.
11. **Report.** See below. Then stop. Don't triage for him.

## Task properties

He triages faster when the properties are already there. Fill them every time, as proposals he can change:

- **Priority**, always set:
  - **1 - Immediate**: safety, regulatory or class matters; anything affecting service; anything due in the next two working days.
  - **2 - Important**: a date this week, a manager or regulator waiting on him, or something blocking someone else's work.
  - **3 - Normal**: the default for real work with no pressure on it.
  - **4 - Low**: ideas, nice-to-haves, "one day" items.
  - **Purchasing**: when the action itself is ordering or buying something.
  - Say in **Suggested handling** why, in a few words: "Priority 2: Jason wants it before Friday."
- **People**: everyone named and resolved (see step 6), including the person he is waiting on.
- **Ships and Docks**, **Areas**, **Projects**: link an existing open project when the task plainly belongs to it.
- **Due Date**: when a deadline was said ("by Friday", "before the 4th", "ahead of the AGM"). Turn it into a real date from the conversation's date; if the phrase is vague ("end of the month"), use the last working day it implies and say so in the body.
- **Do Date**: when he said when he would do it ("I'll call him tomorrow", "Monday morning").
- **Follow-up date**: for things owed to him, when a date was said. If none was said, suggest one in the body only; don't set the property.
- Never set a date that wasn't said or clearly implied. A missing date is better than a false one.

## The cross-check

Every commitment found in a conversation is checked against what is already in Tasks before anything is written, and every open task is checked against what was said. Nothing here changes a task's Status, dates, owner or priority: those are his.

**Searching.** Look by vessel or place, person, and the key words of the action, in two passes: open tasks (any status except Completed and Not completed, To Process included), and tasks closed in the last 60 days. Use `notion-search` within the Tasks data source and SQL on `Name`. A match means the same action on the same thing, not just the same vessel.

**When the commitment is already captured:**
- **Open task:** do not create a new one. Append a dated line to the existing task's body, `Update, <D Mon>. <what was said, to the standard>`, and add the new note to its `Notes`. If a new date or owner was mentioned, put it in that line as "suggested"; leave the properties alone.
- **Closed as Completed:** if it is the same piece of work, do not recreate it; list it in the report under *Already done*. If the problem has come back (a repair that failed again, a recurring request), create a new task, link the old one in `Related Tasks`, and say in **Background** "Recurring: earlier task closed <D Mon>."
- **Closed as Not completed** (binned): do not recreate it unless it was raised again as a fresh commitment. Either way, name it in the report under *Raised again*.

**When a conversation suggests an open task is finished** ("I sent that to Carl", "Rob's replaced the sensors", "that's sorted"):
- Tick `Looks done` on that task and append `Update, <D Mon>. Appears complete: <the evidence, to the standard>.`
- Never set Status to Completed. He confirms in the *Looks done* view on the Second Brain page and clears the box.
- Only on plain evidence. "We should be close" is not done.

**Within the run itself:** the same action raised in two conversations on the same day becomes one task, linked to both notes.

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

- **On demand:** in chat. How many notes and tasks, with links. From the cross-check: how many commitments were already captured (and updated rather than duplicated), the *Looks done* list, *Already done*, *Raised again*, and any *Recurring*. Anything time-sensitive. Anything kept out and why. Anything uncertain enough that he should check it.
- **Nightly:** the run's final message, in the same order, ending with one line: `Intake <date>: <n> notes, <n> new tasks, <n> updated, <n> looks done, <n> kept out, <failures or none>.`

## The count, for the briefing

The morning briefing carries one line: how many tasks are in To Process, how old the oldest is, and how many captures have no note.

```sql
SELECT COUNT(*) AS n, MIN("Created time") AS oldest
FROM "collection://cd94ea0f-20a6-4575-b677-e7ab8a696918"
WHERE "Status" = 'To Process' AND ("Archived" IS NULL OR "Archived" = '__NO__')
```

Flag it when the oldest is more than three days old or the count is over 25.
