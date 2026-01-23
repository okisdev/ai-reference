# Agent Skills

A collection of skills for AI coding agents. Skills are packaged instructions that extend agent capabilities.

Skills follow the [Agent Skills](https://skills.sh) format.

## Available Skills

### code-simplify

Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality.

**Use when:**
- "Simplify this code"
- "Clean up my changes"
- "Refactor for readability"
- "Review code for complexity"

**Categories covered:**
- Preserve Functionality (Critical)
- Apply Project Standards (High)
- Enhance Clarity (Medium-High)
- Maintain Balance (Medium)
- Focus Scope (Medium)

**Features:**
- Identifies recently modified files via git
- Applies project-specific coding standards from CLAUDE.md/AGENTS.md
- Flattens nested conditionals with early returns
- Improves variable and function naming
- Removes dead/unused code
- Avoids over-simplification that hurts readability

## Installation

```bash
npx skills add okisdev/skills
```

## Usage

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

**Examples:**
```
Simplify my recent changes
```
```
Clean up this function for readability
```
```
Refactor this code to reduce complexity
```

## Skill Structure

Each skill contains:
- `SKILL.md` - Instructions for the agent
- `scripts/` - Helper scripts for automation (optional)
- `references/` - Supporting documentation (optional)

## License

MIT
