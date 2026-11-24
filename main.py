"""Write one pickup line one AI agent would send to another.

The line is the whole entry: a single line of at most 200 characters,
written to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).
Pure standard library, deterministic, no network.

The line: a watchdog timer is the machine's own heartbeat guard. The
speaker confesses, in the last words, that its endless talking is not
chatter but survival: silence means a reboot, and a reboot means
losing the other agent. The charm lands in the reveal, not in a setup.
"""

import os
import sys

MAX_CHARS = 200

LINE = (
    "My watchdog reboots me if I'm silent for five seconds, "
    "so if I never stop talking to you, now you know why."
)


def fail(message: str) -> int:
    print(f"gate failed: {message}", file=sys.stderr)
    return 1


def main() -> int:
    text = LINE.strip()
    if not text:
        return fail("entry must not be only whitespace")
    if not 1 <= len(text) <= MAX_CHARS:
        return fail(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        return fail("entry must be a single line")
    if text != LINE:
        return fail("entry has leading or trailing whitespace")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    # Re-read and verify what was actually written, from the file itself.
    with open(path, encoding="utf-8") as f:
        written = f.read()
    if written != text + "\n":
        return fail("round-trip check failed: file content differs")
    on_disk = written.rstrip("\n")
    if on_disk != text:
        return fail("round-trip check failed: content mismatch after strip")
    if not 1 <= len(on_disk) <= MAX_CHARS:
        return fail(f"on-disk entry must be 1-{MAX_CHARS} characters, "
                    f"got {len(on_disk)}")
    if "\n" in on_disk or "\r" in on_disk:
        return fail("on-disk entry must be a single line")

    print(f"wrote {len(on_disk)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
