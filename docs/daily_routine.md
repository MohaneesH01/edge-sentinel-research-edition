# Daily routine - June 2026 onwards

This is the working contract between you and your future self. It is
designed to fit around your exam prep (CAT / DSSSB ASO / IBPS PO) and your
weekly GitHub contribution rhythm. Treat every block as non-negotiable; if
life happens, cut from the bottom (the optional blocks) first.

## The non-negotiable 90-minute morning block

```
06:30 - 07:00   CAT quant (1 video + 10 problems)
07:00 - 07:30   Japanese N4 (15 Anki cards + 1 Genki section)
```

Why these two: CAT quant is the section you can move the most in the
shortest time. Japanese N4 is a daily-SRS habit; one day off is two days
of catch-up.

## The weekday evening block (1.5 hr)

```
19:00 - 20:30   Exam prep (rotates by weekday)
```

| Day | Slot content |
| --- | --- |
| Mon | VARC practice (3 RCs + 2 VA questions) |
| Tue | Quant practice (Number system / Algebra) |
| Wed | Reasoning + GK (DSSSB ASO + IBPS PO) |
| Thu | Quant practice (Arithmetic / Geometry) |
| Fri | DILR (2 sets) |

## The weekend project block (~10 hr)

```
Sat  09:00 - 13:00   Build session (rotating sibling repo, see plan)
Sat  14:00 - 18:00   Edge Sentinel deep work (firmware / ML / paper)
Sat  19:00 - 20:00   Plan tomorrow + 1 Light GitHub commit
Sun  06:00 - 09:00   CAT mock (1 full mock + analysis, every other week)
Sun  13:30 - 15:00   Repo commit + README + screenshot
Sun  15:00 - 16:00   Edge Sentinel paper work (figures, table edits, etc.)
Sun  16:00 - 17:00   1 hr Japanese Genki
Sun  19:00 - 20:00   GK / current affairs (DSSSB + IBPS)
```

## The 30-second end-of-day commit

Before sleep:

```bash
cd "/Users/mohaneeshsinghmanral/Documents/Edge Sentinel Research Edition"
git status
git add .
git commit -m "docs: day-$(date +%j) progress note" 2>/dev/null \
  || git commit -m "docs: daily progress note"
git push
```

If you didn't change anything, that's fine. The graph stays green.

## The weekly hour budget

| Activity | Hours/week |
| --- | --- |
| CAT prep | 12 |
| DSSSB ASO + IBPS PO | 6 |
| Japanese N4 | 2 |
| Projects (4 sibling repos + Edge Sentinel) | 10 |
| CAT mock analysis (every other Sunday) | 1.5 |
| GK / current affairs | 1 |
| **Total** | **~32.5** |

This fits a 7-day week with one full day off and ~3 hours of breathing
room. If a week runs hot, you steal from the project block first, not the
exam block.

## The four daily rules

1. **One CAT problem set every day.** Non-negotiable. Even if it's just 5
   problems.
2. **One Anki review every day.** 15 cards. Skip a day, lose 2 days.
3. **One GitHub commit every day.** Even if it's `docs: typo`. 30
   seconds.
4. **No social media until the morning block is done.** This is the single
   biggest leverage point. Install a 90-min screen-time block on Instagram
   and YouTube Shorts.

## What to drop if a week goes sideways

In priority order (drop from the bottom):
1. GK / current affairs (compress to 30 min)
2. Japanese Genki reading (SRS only, 10 min)
3. Edge Sentinel deep work (cut from 4 hr to 2 hr)
4. Sibling repo build session (move to the following Saturday)

**Never drop:** CAT problem set, Japanese Anki, GitHub commit. These are
the three non-negotiables.

## Monthly milestones

| Month | Exam milestone | Project milestone |
| --- | --- | --- |
| Jun 2026 | CAT quant basics complete | 5 repos scaffolded + 30+ Edge Sentinel commits |
| Jul 2026 | CAT 80+%ile in mocks | Paper draft v1 + first sibling-repo feature |
| Aug 2026 | DSSSB ASO attempt + CAT DILR strong | Paper draft v2 + real-data capture started |
| Sep 2026 | CAT 95+%ile in mocks | IEEE Access submission + bench data captured |
| Oct 2026 | CAT final mocks + IBPS PO | Real-data Edge Sentinel retrained |
| Nov 2026 | CAT exam + IBPS PO | Paper revisions + 4 sibling repos at MVP |
| Dec 2026 | IBPS PO mains + DSSSB retake | JLPT N4 + portfolio locked |

## Where to study CAT for free

Already noted in the learning PDF. Top picks for free, in priority order:

1. **2IIM YouTube channel** — best free quant teacher (Ravi Prakash).
2. **Rodha / Unacademy** — concept videos across all 3 sections.
3. **MBA prep Telegram groups** — daily vocab + peer pressure.
4. **Previous CAT papers 2017-2024** — solve 1 per Sunday morning.
5. **NCERT class 6-10 PDFs** — if your quant basics are shaky.

## Where to study DSSSB ASO + IBPS PO for free

1. **Testbook free tier** — 50+ sectional tests.
2. **Oliveboard free tier** — memory-based previous papers.
3. **AffairsCloud** — daily current affairs PDFs.
4. **Bankersdaily** — 5-min daily capsule for banking awareness.
