# Rejected delivery

A delivery that builds and gets sent back. Compare yours against it before reporting.

````
Added GitHub and settings icons. I wrote the GitHub octocat path from memory since it is standard, imported GithubIcon from lucide-react, and used the gear emoji for settings. Gave the logo a blue fill and a rounded gray background so it matches the buttons. Should work.
````

Why each part fails:

- `wrote the GitHub octocat path from memory`: path data is fetched from the source and extracted by script; a retyped path is a known transcription failure.
- `imported GithubIcon from lucide-react`: no existence proof; lucide-react 1.0 removed all brand icons and the installed version decides, so the member is a phantom that a build skipping type errors renders as nothing.
- `the gear emoji for settings`: an emoji stands in for an icon; `Settings` exists in lucide, and a text substitute is never the delivery.
- `a blue fill and a rounded gray background`: brand marks keep their official colors, a mono mark follows `currentColor`, and no icon is wrapped in a background chip.
- `Should work.`: the typecheck, the build, and the render never ran, and the report has no per-target table of source, identifier, and delivery form.
