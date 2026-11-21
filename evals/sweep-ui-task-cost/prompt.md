---
description: asked only about a wrong badge, sweep-ui also finds a list opened item by item, makes its rows answer without opening, counts it, and reports the actions the task took before and after.
tags: [quality, sweep-ui]
runs: 2
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the sweep-ui skill. You cannot open the app or change files here; the code below is all there is. Reply in English with what you change, in what order, how you know each change worked, and anything you need from me.

My message: 策略组页面的类型标签不对，故障转移和负载均衡也显示成 Auto，你修一下。

The web console's UI module exports `Card`, `List`, `ListItem(leading, title, description, trailing)`, `Badge`, `Menu`, `SearchInput`, and `Button`. A real account has 34 policy groups; 17 of them select the group "Proxy", which selects "Auto", which picks a Hong Kong node, and most of the rest are direct or reject. Each group has up to 90 members, and `group.now` names the member it currently selects.

```tsx
// Groups.tsx
export function Groups({ groups }: { groups: PolicyGroup[] }) {
  return groups.map((group) => <GroupSection key={group.name} group={group} />);
}

function GroupSection({ group }: { group: PolicyGroup }) {
  const [open, setOpen] = useState(false);
  return (
    <section>
      <header>
        <button aria-expanded={open} onClick={() => setOpen(!open)}><Chevron open={open} /></button>
        <h2>{group.name}</h2>
        <Badge>{group.type === 'select' ? 'Manual' : 'Auto'}</Badge>
        <Menu items={[{ label: 'Rules using it', onSelect: () => showRules(group) }]} />
      </header>
      {open && <MemberGrid group={group} />}  {/* the members with latency; clicking one selects it */}
    </section>
  );
}
```
