# Terminal harness lifecycle

All scratch files (transcripts, logs) go in the session scratchpad, not the repo.

## tmux session

```bash
S="verify-cli-$$"
tmux new-session -d -s "$S" -x 120 -y 32 -e TERM=xterm-256color <command-under-test>
tmux capture-pane -pt "$S" > "$SCRATCH/00-initial.txt"
```

Fixed `-x`/`-y` makes layout captures reproducible; state the size in the report because TUI layout claims are size-relative.

## Drive and capture

One action, then a bounded poll for a concrete pattern, then a capture:

```bash
tmux send-keys -t "$S" "help" Enter

i=0; until tmux capture-pane -pt "$S" | grep -q "<expected-pattern>"; do
  i=$((i+1)); test "$i" -ge 30 && break; sleep 1
done
tmux capture-pane -pt "$S" > "$SCRATCH/01-after-help.txt"
```

Special keys use tmux key names: `Enter`, `Escape`, `Up`, `Down`, `Tab`, `C-c`, `BSpace`. Send literal text and the key in one call (`send-keys -t "$S" "text" Enter`). On poll expiry the last capture is the failure evidence; kill the session and report.

Resize mid-session to test reflow:

```bash
tmux resize-window -t "$S" -x 60 -y 20
```

## Baseline and treatment

Capture the same scripted sequence twice, from the pre-change and post-change states, into parallel numbered files, then:

```bash
diff "$SCRATCH/baseline/03-final.txt" "$SCRATCH/treatment/03-final.txt"
```

Identical command, inputs, warmup, size, and env; only the code under test changes.

## Teardown

```bash
tmux kill-session -t "$S"
```

Only the session this run created. Never `pkill` or kill by name.

## PTY fallback (no tmux)

For a non-interactive transcript, `script` gives the CLI a real PTY:

```bash
script -q "$SCRATCH/transcript.txt" <command> </dev/null
```

For interactive flows without tmux, a short Python driver:

```python
import pty, os, time, sys
pid, fd = pty.fork()
if pid == 0:
    os.execvp(sys.argv[1], sys.argv[1:])
def read_until(pattern, budget=30.0):
    out, end = b"", time.time() + budget
    while time.time() < end and pattern not in out:
        try:
            out += os.read(fd, 4096)
        except OSError:
            break
    return out.decode(errors="replace")
print(read_until(b"> "))
os.write(fd, b"help\n")
print(read_until(b"> "))
os.kill(pid, 15)
```

## Timing claims

Time-to-first-prompt: start the session, poll for the prompt pattern, and report the loop count as seconds-granularity timing. For anything finer, wrap the non-interactive path in `time` and compare baseline against treatment on the same machine in the same run.
