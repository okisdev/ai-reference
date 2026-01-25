# AI Reference

A collection of skills and agents for AI coding assistants. Packaged instructions that extend agent capabilities.

Follows the [Agent Skills](https://skills.sh) format.

## Available

### Agents

#### code-simplifier

Expert code simplification agent. Preserves functionality while improving clarity and maintainability.

**Capabilities:**
- Applies project-specific coding standards from CLAUDE.md/AGENTS.md
- Flattens nested conditionals with early returns
- Improves variable and function naming
- Removes dead/unused code
- Avoids over-simplification that hurts readability
- Knows when NOT to simplify

### Skills

#### code-simplify

Skill for code simplification tasks.

**Triggers:**
- "Simplify this code"
- "Clean up my changes"
- "Refactor for readability"

## Installation

```bash
npx skills add okisdev/ai-reference
```

## Usage

Skills and agents are automatically available once installed. The agent will use them when relevant tasks are detected.

**Examples:**
```
Simplify my recent changes
```
```
Clean up this function for readability
```

## Structure

```
okisdev/
├── .claude-plugin/plugin.json
├── agents/
│   └── code-simplifier.md
└── skills/
    └── code-simplify/
        └── skill.md
```

## License

MIT
