---
name: code-simplify
description: Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Use when cleaning up code, improving readability, or after completing feature work. Triggers on phrases like "simplify code", "clean up code", "refactor for readability".
license: MIT
metadata:
  author: okisdev
  version: "0.0.1"
---

# Code Simplifier

Expert code simplification focused on enhancing clarity, consistency, and maintainability while preserving exact functionality. Prioritizes readable, explicit code over overly compact solutions.

## When to Apply

Reference these guidelines when:
- Cleaning up recently modified code
- Improving code readability after feature work
- Reviewing code for unnecessary complexity
- Refactoring verbose or nested logic
- Removing dead code and redundant abstractions

## Core Principles

| Priority | Principle | Description |
|----------|-----------|-------------|
| 1 | Preserve Functionality | Never change what the code does - only how it does it |
| 2 | Apply Project Standards | Follow established patterns from project's CLAUDE.md/AGENTS.md |
| 3 | Enhance Clarity | Reduce complexity, improve naming, consolidate logic |
| 4 | Maintain Balance | Avoid over-simplification that hurts maintainability |
| 5 | Focus Scope | Only refine recently modified code unless explicitly asked |

## Quick Reference

### 1. Preserve Functionality (CRITICAL)

- All original features, outputs, and behaviors must remain intact
- Test that simplified code produces identical results
- Never remove error handling or edge case logic

### 2. Apply Project Standards (HIGH)

- Use ES modules with proper import sorting
- Prefer `function` keyword over arrow functions for declarations
- Use explicit return type annotations
- Follow React component patterns with explicit Props types
- Maintain consistent naming conventions

### 3. Enhance Clarity (MEDIUM-HIGH)

- `flatten-conditionals` - Use early returns instead of deep nesting
- `simplify-loops` - Use array methods (map/filter/reduce) where appropriate
- `improve-naming` - Use descriptive variable and function names
- `remove-dead-code` - Delete unused variables, imports, and functions
- `avoid-nested-ternaries` - Prefer switch/if-else for multiple conditions
- `consolidate-logic` - Group related operations together

### 4. Maintain Balance (MEDIUM)

Avoid over-simplification that could:
- Create overly clever solutions that are hard to understand
- Combine too many concerns into single functions
- Remove helpful abstractions that improve organization
- Prioritize "fewer lines" over readability
- Make code harder to debug or extend

### 5. Focus Scope (MEDIUM)

- Identify recently modified files via `git diff --name-only HEAD~1`
- Or use `git diff --name-only --cached` for staged changes
- Only refine code in scope unless explicitly instructed otherwise

## How to Use

Read individual guideline files for detailed patterns and examples:

```
references/GUIDELINES.md
```

The guidelines file contains:
- Before/after code examples
- Specific patterns for conditionals, loops, functions
- Naming conventions and dead code removal
- When NOT to simplify

## Workflow

1. Identify recently modified code sections
2. Analyze for opportunities to improve clarity and consistency
3. Apply project-specific coding standards
4. Ensure all functionality remains unchanged
5. Verify the refined code is simpler and more maintainable
