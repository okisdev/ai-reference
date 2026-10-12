# Rejected body

A draft that compiles into a PR and still gets rewritten by the user. Compare yours against it before creating.

````
Title: Feat: Add Recap Activity Skill

## Summary

This PR adds a new skill - it lets you recap activity across GitHub, Vercel
and the local machine, which is super useful for weekly reports.

- [x] Tested
- [x] Works on Linux

Closes #12

[a Co-Authored-By trailer naming a coding tool]
````

Why each part fails:

- `Feat: Add Recap Activity Skill`: the title is lowercase after the type; Title Case reads as a template.
- `## Summary`: section headings are lowercase.
- `skill - it lets you`: a hyphen used as sentence punctuation; break with a period, semicolon, or comma.
- The paragraph is hard-wrapped at 76 columns; a paragraph stays on one line.
- `super useful for weekly reports`: sells instead of naming the mechanism a reviewer checks.
- `- [x] Tested` and `- [x] Works on Linux`: pre-checked without the command or the result it showed, and the second was never run; check only what was verified, with its command and outcome.
- `Closes #12` at the bottom: the closes line comes first, with a lowercase keyword.
- The trailer: no trace of how the PR was made (seen: tool trailers and session links the user had to strip from merged PRs).
