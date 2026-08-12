---
name: clip
description: Copy text to the macOS clipboard via pbcopy so the user can paste it cleanly, instead of selecting it out of the terminal where line-wrapping, the 2-space wrapped-list indent, and timestamps get baked into the selection. Use this whenever the user says "copy that", "put it on my clipboard", "pbcopy this", "copy to clipboard", "clip that", or otherwise wants something you just wrote (a summary, a list, a command, a code block, a message draft) made paste-ready — even if they don't name pbcopy explicitly. Especially relevant right after producing a Teams/Slack/email draft or any multi-line block the user will paste somewhere else.
---

# clip — copy text to the macOS clipboard

The terminal is a bad copy source: it wraps long lines, adds a 2-space indent to wrapped list-item continuations, and mixes in prompt/timestamp chrome. When the user wants to paste something you produced into Teams, Slack, an email, a doc, etc., the clean move is to push the exact text to the clipboard with `pbcopy` rather than making them hand-select it.

## What to copy

Usually the user means "the thing you just wrote" — the most recent summary, draft, list, or code block. If that's ambiguous (you produced several blocks), ask which one, or copy the most likely candidate and say what you copied. If the user supplies or points at specific text, copy that verbatim.

Copy the **raw content** the user will actually paste — not your surrounding commentary, and not markdown scaffolding they don't want. For a chat/email draft, that's the message body. For a shell command, that's just the command. Match what they'd expect to land in the destination.

## How to copy it (preserve formatting exactly)

Pipe the text to `pbcopy` through a **quoted heredoc**. Quoting the delimiter (`'CLIP_EOF'`) tells the shell to pass everything through literally — no variable expansion, no backtick execution, no escaping of `$`, `"`, `\`, emoji, or unicode. This is what keeps the text from getting mangled.

```bash
cat <<'CLIP_EOF' | pbcopy
<the exact text to copy, multiple lines, emoji, bullets — all fine>
CLIP_EOF
```

Then confirm in one line, e.g. `✅ Copied to clipboard (12 lines).` A quick verification that doesn't dump the whole payload back into the conversation:

```bash
cat <<'CLIP_EOF' | pbcopy
...content...
CLIP_EOF
printf '✅ Copied %s lines, %s chars\n' "$(pbpaste | wc -l | tr -d ' ')" "$(pbpaste | wc -c | tr -d ' ')"
```

## Two things that actually break this

1. **Delimiter collision.** A quoted heredoc ends at the first line that is *exactly* the delimiter. If the content could contain a bare line reading `CLIP_EOF`, pick a delimiter you can see isn't present in the text (e.g. `CLIP_EOF_9f3`). Glance at the content first.
2. **Trailing newline.** A heredoc appends a final newline, so the clipboard ends with one. That's almost always fine (and often desirable) for pasting into chat/docs. If the user needs *no* trailing newline — e.g. copying a value into a password field or a CSV cell — use `printf '%s'` with the content single-quoted instead, so nothing extra is added:

   ```bash
   printf '%s' 'exact value with no trailing newline' | pbcopy
   ```

## Notes

- This is macOS-only (`pbcopy`/`pbpaste`). The user is on darwin, so that's the default and fine.
- Don't echo the full copied text back as a confirmation — the point was to get it out of the scrollback. A line/char count is enough proof it worked.
