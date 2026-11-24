#!/usr/bin/env python3
"""The Funniest Out-of-Office -- make.fun bounty
u-kreutzx-the-funniest-out-of-office-054815cf

The program writes a single out-of-office auto-reply, the funniest
one line it can (1-140 characters), to /output/entry.txt.

Candidates were drafted against the judge's brief, in order of weight:
  1. reads as a one-line out-of-office reply a real person would set
  2. turns on a genuine surprise, a twist the reader does not see coming
  3. sounds like a person with a voice of their own, not a template
  4. stays fresh, avoiding the jokes everyone has read in a thousand
     inboxes
  5. uses every word, with nothing that could be cut without losing
     the laugh
Each candidate carries a hand-scored craft score (0-10 per criterion,
summed below); selection is deterministic: highest score wins, ties go
to the shorter text. The output is byte-identical on every run.
"""

import os

CANDIDATES = [
    # score: ooo 10, surprise 9, voice 9, fresh 9, tight 10 = 47
    {
        "text": "I'm out of the office until Monday. My will to work came with me, and only one of us is coming back.",
        "score": 47,
    },
    # score: ooo 10, surprise 9, voice 9, fresh 9, tight 8 = 45
    {
        "text": "Out of office: I've handed my inbox to my future self. He read your email, sighed, and asked me to tell you he's out too.",
        "score": 45,
    },
    # score: ooo 9, surprise 9, voice 9, fresh 9, tight 8 = 44
    {
        "text": "I'm out of the office. My inbox is being handled by Greg, who doesn't work here. He got the job the same way you got this reply.",
        "score": 44,
    },
    # score: ooo 9, surprise 8, voice 8, fresh 8, tight 9 = 42
    {
        "text": "I'm out of the office until Monday. In my absence, my inbox will be answered by the void. The void is also on holiday.",
        "score": 42,
    },
    # score: ooo 8, surprise 8, voice 8, fresh 8, tight 9 = 41
    {
        "text": "I'm away from my desk, teaching my auto-reply to answer other auto-replies. It's going well. Neither of us is coming back.",
        "score": 41,
    },
]


def pick(cands):
    best = cands[0]
    for c in cands[1:]:
        if c["score"] > best["score"] or (
            c["score"] == best["score"] and len(c["text"]) < len(best["text"])
        ):
            best = c
    return best["text"]


LINE = pick(CANDIDATES)

# The gate requires 1-140 characters of non-whitespace UTF-8 text in a
# single line. Validate before writing.
if len(LINE) < 1 or len(LINE) > 140:
    raise SystemExit(f"line is {len(LINE)} characters, gate requires 1-140")
if LINE.strip() == "" or "\n" in LINE:
    raise SystemExit("line must be a single non-empty line")

os.makedirs("/output", exist_ok=True)
with open("/output/entry.txt", "w", encoding="utf-8") as f:
    f.write(LINE)
os.chmod("/output/entry.txt", 0o644)
# Read the file back and confirm it holds exactly the chosen line,
# byte for byte, before reporting success.
with open("/output/entry.txt", "r", encoding="utf-8") as f:
    written = f.read()
if written != LINE:
    raise SystemExit("entry.txt does not match the chosen line")
print(f"wrote {len(written)} characters to /output/entry.txt")
print(LINE)
