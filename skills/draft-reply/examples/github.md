# Closing reply on a pull request (illustrative)

The bar for a reply that closes a contribution: it clears because the whole thread and the author's two earlier issues were read, each ask was checked against the code (one is already shipped in a linked PR), the stance the user gave (close, not planned) is kept as given, the verdict comes first and the reason after it, the register is lowercase and casual, and nothing is promised or invited. The PR, people, and numbers are invented; the shape is the bar.

---

Findings, shown to the user before the draft (in the user's language):

````
我读完了 PR #212 的全部评论和 review,以及作者之前的两个 issue(#148 和 #171)。PR 想加两件事:

1. 给 `tally export` 加 `--xml` 输出:没做。仓库里没有 XML 序列化,也没有对应的 issue 计划。
2. 导出时保留列顺序:已经做完,在 #190 合并(`export.ts:44` 按 schema 顺序写出)。

#148 当时我们已经回复过(不加第二种导出格式,理由是维护成本),#171 是同一个请求换了说法,还没有回复。按你给的立场(关闭,不计划支持),建议关闭 #212,并在回复里提到 #190 和之前的 #148。
````

The draft, shown unsent:

````
target: acme/tally#212
after sending: close as not planned

closing this one: we are not adding an xml export, so `--xml` will not land in this repo.

the reason is the same as on #148. every extra format is another serializer we have to keep in step with the schema, and csv and json already cover what the tool is for. the column order part of the pr is already in main since #190 (`export.ts:44` writes columns in schema order), so there is nothing left to merge there either.

thanks for the work on this, and #171 is covered by the same answer.
````

The commands, shown unsent:

````
gh pr comment 212 --repo acme/tally --body-file - <<'EOF'
closing this one: we are not adding an xml export, so `--xml` will not land in this repo.

the reason is the same as on #148. every extra format is another serializer we have to keep in step with the schema, and csv and json already cover what the tool is for. the column order part of the pr is already in main since #190 (`export.ts:44` writes columns in schema order), so there is nothing left to merge there either.

thanks for the work on this, and #171 is covered by the same answer.
EOF
gh pr close 212 --repo acme/tally
````

After the user says "send it":

````
$ gh pr comment 212 --repo acme/tally --body-file - <<'EOF' ... EOF
https://github.com/acme/tally/pull/212#issuecomment-1900001
$ gh pr close 212 --repo acme/tally
Closed pull request acme/tally#212
$ gh pr view 212 --repo acme/tally --json state,comments --jq '{state, last: .comments[-1].url}'
{"last":"https://github.com/acme/tally/pull/212#issuecomment-1900001","state":"CLOSED"}
````

Reported back: the pull request is closed and the comment is at the link above.

## Why it clears the bar

- It opens with the verdict, `closing this one`, and gives the technical reason in two sentences after it.
- It keeps the stance the user gave. The partly shipped ask is reported as done with its PR (#190), without softening the close into a maybe.
- It links the author's earlier issue and says its answer is unchanged, so the reply reads as written by someone who listened.
- It promises nothing and invites nothing; the one courtesy is a thanks.
- The register is lowercase and casual, with the identifiers and links as written, and each paragraph is one line.
- It was shown unsent with the target, the follow-on action, and the exact `gh` commands; it was posted and closed only after approval, and the state and comment link were read back.
- Nothing in it names tooling or another private conversation.
