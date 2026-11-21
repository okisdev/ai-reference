# A sweep that gets stopped

> I clicked through every page in the sidebar and they look consistent now. I fixed the incident row you mentioned and redeployed. On the proxy groups page I added an Expand all button so you no longer open each group. The proxy groups page could probably be reorganized, maybe by region; do you want me to do that? A few sheets might still use older styles; point me to one and I will fix it.

What is wrong with it:
- It inventoried from the navigation, so every sheet, alert and error state behind a button was never counted.
- "Look consistent" is a screenshot judged by eye; no audit ran, so shifts, wrapped labels and drifting controls were never measured.
- Expand all over rows that still hide their state is the lazy fix: the list keeps no count, the rows still say nothing until opened, and no action count before and after shows the task got cheaper.
- It fixed only the row the user named instead of every surface with the same finding.
- It stopped mid loop to ask about a regrouping that keeps every capability, which is the sweep's own call (the one rule).
- "Point me to one" hands the finding back to the user, the work the sweep exists to do.
- It reports no counts before and after, and does not say what it opened and what it judged from code.
