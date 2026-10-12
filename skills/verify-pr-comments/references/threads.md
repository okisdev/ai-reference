# Review thread read

Invoked from verify-pr-comments step 2 and from approve-pr step 4. `reviewThreads` is GraphQL-only, and one query returns at most 100 threads, so a PR with more loses every thread past the hundredth. Loop on `pageInfo` until `hasNextPage` is false.

Parameterize `<owner>`, `<repo>`, and `<num>`; `-F` sends the number as a JSON Int.

```bash
set -o pipefail
cursor=null
while :; do
  page=$(gh api graphql -F owner=<owner> -F repo=<repo> -F num=<num> -F cursor="$cursor" -f query='
    query($owner: String!, $repo: String!, $num: Int!, $cursor: String) {
      repository(owner: $owner, name: $repo) {
        pullRequest(number: $num) {
          reviewThreads(first: 100, after: $cursor) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id
              isResolved
              isOutdated
              path
              line
              comments(first: 100) {
                nodes { databaseId author { login } body createdAt }
              }
            }
          }
        }
      }
    }') || exit 1
  printf '%s\n' "$page" | jq -c '.data.repository.pullRequest.reviewThreads.nodes[]'
  cursor=$(printf '%s\n' "$page" | jq -r '.data.repository.pullRequest.reviewThreads.pageInfo | select(.hasNextPage) | .endCursor')
  [ -n "$cursor" ] || break
done
```

The loop prints one compact JSON thread per line. Filter it by piping `done` into `jq -s`, for example `done | jq -s '[.[] | select(.isResolved == false)] | length'` for the unresolved count. A comment's `databaseId` is its REST id, which joins a thread to the inline comments from `pulls/<num>/comments`.
