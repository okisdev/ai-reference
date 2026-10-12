# Rejected plan

A chart plan that reads fine and gets sent back. Compare yours against it before writing the catalog.

````
Plan: add recharts and a shared Chart wrapper. Overview gets a line chart of requests, a pie of requests by provider, a bar chart of cost by model, and a gauge for error rate, each tile with a sparkline. Project pages get the same charts again. Charts animate in on load. I will wire the data once the components look right.
````

Why each part fails:

- `add recharts and a shared Chart wrapper`: the plan starts from a library and then looks for something to draw; the engine is a fork decided after the forms are chosen (seen: asks about text-heavy screens went to a chart library before deciding what to show).
- A chart per metric with no question: the question picks the form and the title is the question; no catalog row names a source, a tier, or what production says.
- `a pie of requests by provider`: a pie or donut is rejected when most groups collapse to one or two slices, and the cardinality per tenant was never read or the id spellings folded.
- `a gauge for error rate`: a meter answers how close to a limit, an error rate answers whether something is changing, and a status that is never written would read 0.0% forever; unknown is never zero.
- `each tile with a sparkline`: a tile carries a window, a comparison, and a denominator, and a sparkline only where a real per-bucket series exists; without them it is a key/value row.
- `the same charts again` on project pages: the overview summarizes and links onward, the detailed chart stays on the subject page, and every mark links to the row-level view it summarizes.
- `Charts animate in on load`: no entrance animation on any chart.
- `wire the data once the components look right`: no chart component for a data shape the app does not have, and a chart whose table is empty in production is an empty state that names how to fill it.
- No Not built list: every killed candidate is listed with its reason, or the next pass redraws it.
