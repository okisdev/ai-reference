# Chat reply to a teammate (illustrative)

The bar for a chat thread: the analysis goes to the user in the user's language with each ask sorted into done, in progress, and not started, then the reply is short, unheaded, casual, in the teammate's language, and held until approved. The people, channel, and links are invented; the shape is the bar.

---

The thread, read from where the topic starts:

````
#team-billing, thread started by Mira Lindqvist
mira: is the invoice pdf export done? the pilot customer asks on thursday
mira: also does it handle multiple currencies
````

The analysis, shown to the user before the draft:

````
我读了整个 thread,并对照了代码和 PR。Mira 问的是 PDF 导出做完没有,以及是否支持多币种:

- 已完成:单币种发票导出,在 #318 合并,周二已发布(https://github.com/acme/billing/pull/318)。
- 进行中:多币种,PR #331 还是 draft,汇率取整的测试没过(https://github.com/acme/billing/pull/331)。
- 未开始:周四给试点客户用的批量导出,没有对应的 issue 或分支。

所以对 "做完了吗" 的诚实回答是:单币种做完了,多币种在路上,批量没开始。你没给立场,我的建议是如实说,不承诺日期。
````

The draft, shown unsent:

````
target: Slack thread in #team-billing, reply to Mira Lindqvist
after sending: none

single currency export is done and live since tuesday (<https://github.com/acme/billing/pull/318|#318>). multi currency is in progress, the pr is still a draft because the rounding tests fail (<https://github.com/acme/billing/pull/331|#331>). bulk export is not started.

so for thursday the pilot customer can have single currency pdfs, not the rest.
````

Held for approval: nothing is sent until the user says so. On approval it goes through the messaging tool's send call, the sent message is read back, and its link is reported.

## Why it clears the bar

- The analysis is in the user's language and sorts every ask into done, in progress, or not started, each with its link, before any draft exists.
- The reply is two short paragraphs with no headings, the way a person talks to a teammate, in the thread's language.
- It uses Slack mrkdwn links and nothing else of the markup.
- It says what is true, including that two of the asks are not finished, and promises no date.
- It was held for approval with its target and the send call named.
