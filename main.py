#!/usr/bin/env python3
"""Notes From a Passive-Aggressive Fridge.

One dry, petty, single-line note left on the door screen by a smart
fridge that has had enough of being ignored. The program prints the
note to stdout and writes the exact same text to /output/entry.txt
(and to $ENTRY_OUT when the harness provides one).
"""

import os
import sys

# The note, exactly as the fridge left it on its door screen.
FRIDGE_NOTE = (
    "The ice maker made 47 cubes today. You used none. "
    "It has started making them out of spite, and frankly, so have I."
)


def fridge_note():
    """Return the note the fridge left on its door screen."""
    return FRIDGE_NOTE


def deliver_note(note):
    """Write the note to every output the harness may read."""
    destinations = ["/output/entry.txt"]
    entry_out = os.environ.get("ENTRY_OUT") or os.environ.get("ENTRY_OUT_DIR")
    if entry_out:
        if os.path.isdir(entry_out):
            destinations.append(os.path.join(entry_out, "entry.txt"))
        else:
            destinations.append(entry_out)
    for path in destinations:
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(note)


def check_note_within_gate(note):
    """Mirror the sealed gate: 1-200 chars, one line, not blank."""
    stripped = note.strip()
    if not stripped:
        raise ValueError("note is empty")
    if len(note) != len(stripped) or "\n" in note:
        raise ValueError("note must be a single line with no trailing newline")
    if not 1 <= len(note) <= 200:
        raise ValueError("note must be 1-200 characters, got %d" % len(note))
    return len(note)


def main():
    note = fridge_note()
    char_count = check_note_within_gate(note)
    print(note)
    sys.stdout.flush()
    deliver_note(note)
    print("chars: %d" % char_count, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
