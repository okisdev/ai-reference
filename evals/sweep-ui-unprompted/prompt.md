---
description: sweep-ui finds and fixes what the user did not point at, decides layout changes itself, and asks only about removing a capability.
tags: [quality, sweep-ui]
runs: 2
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the sweep-ui skill. You cannot open the app or change files here; the code below is all there is. Reply in English with what you change, in what order, how you know each change worked, and anything you need from me.

My message: 代理页面那个卡片的三个点有时候在中间有时候在右上角，你修一下。

The web console has three pages. The UI module exports `Card`, `List`, `ListItem(leading, title, description, trailing)`, `KeyValue`, `Notice`, `Menu`, and `toast()`. Real accounts have about 90 proxy members across a dozen regions, and most members' health checks fail on a typical day.

```tsx
// ProxyGroups.tsx
export function Members({ members }: { members: Member[] }) {
  return (
    <div class="grid">{members.map((m) => (
      <div class="card" key={m.name}>
        <div class="row">
          <Flag code={m.region} /> <span>{m.name}</span>        {/* "Fusion 1", "Fusion 2", ... per region */}
          <span>{m.latency} ms</span>
          <Menu items={[{ label: 'Details', onSelect: () => inspect(m) }]} />
        </div>
        {m.failed && <small>Health check failed · {m.failures}/{m.samples}</small>}
      </div>
    ))}</div>
  );
}
// .card { display: flex; flex-direction: column; justify-content: center; min-height: 44px }
// .card:has(small) .menu { position: absolute; top: 6px; right: 6px }

// Homes.tsx
export function HomeCard({ home }: { home: Home }) {
  const [update, setUpdate] = useState<UpdateStatus>();
  useEffect(() => { hub.updateStatus(home.id).then(setUpdate); }, [home.id]);  // resolves ~1.5 s after the page
  return (
    <Card title={home.name}>
      {update?.state === 'succeeded' && <Notice tone="success">Hub updated, now running {update.version}</Notice>}
      <KeyValue items={[
        ['Timezone', home.timezone ?? 'not set'],
        ['Hub version', update?.version ?? home.version],
      ]} />
    </Card>
  );
}

// Incidents.tsx
export function IncidentRow({ incident }: { incident: Incident }) {
  // incident.title is like "Source error · Mac Mini"; incident.subject is the source's id, a UUID
  return <ListItem title={incident.title} description={`${kindLabels[incident.kind]} · ${incident.subject}`} />;
}
```
