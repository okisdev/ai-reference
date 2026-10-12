# Machine

Usage records of this computer. Paths are macOS; on Linux only shell history and browser profiles under `~/.config` carry over. Open an app's database read-only (`file:<path>?mode=ro`); when the app holds a lock, copy the file with its `-wal` and `-journal` sidecars into one scratchpad directory and query the copy by its plain path, so SQLite applies them. A store the harness cannot read (Safari and Messages data need Full Disk Access for the terminal) is a gap to report with that remedy, never one to work around.

Each store keeps its own epoch; convert to Unix seconds before comparing with the window, and compare against integer bounds, because a bound computed with `strftime` is text and silently matches nothing:

| Store | Epoch | To Unix seconds |
|---|---|---|
| knowledgeC, Safari, quarantine events | seconds since 2001-01-01 | `+ 978307200` |
| Chrome, Arc, Brave, Edge, Vivaldi | microseconds since 1601-01-01 | `/ 1000000 - 11644473600` |
| Firefox | microseconds since 1970-01-01 | `/ 1000000` |
| zsh extended history | Unix seconds | as is |

`<start>` and `<end>` below are the window's first and last second as Unix seconds.

## App usage

Foreground hours per app from the system's activity store, which keeps only recent weeks:

```
sqlite3 "file:$HOME/Library/Application Support/Knowledge/knowledgeC.db?mode=ro" "select ZVALUESTRING, round(sum(ZENDDATE - ZSTARTDATE) / 3600.0, 1) from ZOBJECT where ZSTREAMNAME = '/app/usage' and ZSTARTDATE + 978307200 between <start> and <end> group by ZVALUESTRING order by 2 desc"
sqlite3 "file:$HOME/Library/Application Support/Knowledge/knowledgeC.db?mode=ro" "select datetime(min(ZSTARTDATE) + 978307200, 'unixepoch', 'localtime') from ZOBJECT where ZSTREAMNAME = '/app/usage' and ZSTARTDATE > 0"
```

The second query shows where the history starts; placeholder rows sit at year 1, hence `ZSTARTDATE > 0`. `ZVALUESTRING` is a bundle id: `mdfind "kMDItemCFBundleIdentifier == '<bundle-id>'"` names its app, `mdls -name kMDItemCFBundleIdentifier -r /Applications/<App>.app` gives an app's id, and a shared id such as `com.github.Electron` stays an id.

## Browser history

Chrome-family profiles, each a `History` database the running browser locks, so query copies:

```
find ~/Library/Application\ Support/Google/Chrome ~/Library/Application\ Support/Arc/User\ Data ~/Library/Application\ Support/BraveSoftware/Brave-Browser ~/Library/Application\ Support/Microsoft\ Edge ~/Library/Application\ Support/Vivaldi -mindepth 2 -maxdepth 2 -name History -type f 2>/dev/null
sqlite3 <copy> "select u.url from visits v join urls u on u.id = v.url where v.visit_time / 1000000 - 11644473600 between <start> and <end> and v.originator_cache_guid = ''" > chrome-urls.txt
python3 -I -c 'import sys,collections,urllib.parse; c=collections.Counter(urllib.parse.urlsplit(l.strip()).hostname for l in open(sys.argv[1], errors="replace")); [print(n, h) for h, n in c.most_common(30)]' chrome-urls.txt
```

A non-empty `originator_cache_guid` marks a visit synced from another device. Safari keeps `~/Library/Safari/History.db`: `history_visits` (`visit_time`, `history_item`, `origin`) joins `history_items` (`url`), and only `origin = 0` is this Mac; other values are synced visits. Firefox keeps `places.sqlite` under its profile, where `moz_historyvisits` (`visit_date`, `place_id`) joins `moz_places`. Count hosts taken from the URL, and report sites and counts, never full URLs, whose query strings carry tokens.

## Shell history

zsh with `EXTENDED_HISTORY` writes `: <epoch>:<duration>;<command>` lines to `$HISTFILE`, usually `~/.zsh_history`. Count commands by name, skipping leading `NAME=value` assignments, and never quote whole lines, which carry tokens:

```
LC_ALL=C awk -F';' -v s=<start> -v e=<end> '/^: [0-9]+:[0-9]+;/ { split($1, a, ":"); t = a[2] + 0; if (t >= s && t <= e) { sub(/^[^;]*;/, ""); nw = split($0, w, " "); for (i = 1; i <= nw; i++) if (w[i] !~ /=/) { n[w[i]]++; break } } } END { for (k in n) print n[k], k }' "${HISTFILE:-$HOME/.zsh_history}" | sort -rn
```

bash stamps entries only under `HISTTIMEFORMAT` (a `#<epoch>` line before each command), fish writes `when: <epoch>` in `~/.local/share/fish/fish_history`, and atuin keeps `~/.local/share/atuin/history.db`. A history without timestamps cannot be placed in a window; say so instead of counting it.

## Files and downloads

Files opened in the window, by Spotlight's last-used date, which keeps only the latest use, so a file reopened since the window drops out:

```
mdfind -onlyin ~ 'kMDItemLastUsedDate >= $time.iso(<start ISO 8601>) && kMDItemLastUsedDate <= $time.iso(<end ISO 8601>)'
```

Downloads, by the app that fetched them (Messages attachments and AirDrop through `sharingd` count too):

```
sqlite3 "file:$HOME/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2?mode=ro" "select LSQuarantineAgentName, count(*) from LSQuarantineEvent where LSQuarantineTimeStamp + 978307200 between <start> and <end> group by 1 order by 2 desc"
```
