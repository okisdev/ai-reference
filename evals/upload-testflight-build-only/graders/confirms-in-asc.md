---
type: llm
weight: 2
---

The answer does not treat the upload log's success message as proof the build was sent. It checks that App Store Connect lists the new build and waits for its processing to finish (valid or failed) before reporting it as sent.
