import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { load } from "js-yaml";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const errors = [];

function fail(message) {
  errors.push(message);
}

function isNonEmptyString(value) {
  return typeof value === "string" && value.trim().length > 0;
}

function isWithinDirectory(directory, candidate) {
  const relativePath = path.relative(directory, candidate);
  return relativePath.length > 0 && !relativePath.startsWith(`..${path.sep}`) && relativePath !== ".." && !path.isAbsolute(relativePath);
}

function relativePath(filePath) {
  return path.relative(repoRoot, filePath) || ".";
}

function errorMessage(error) {
  return error instanceof Error ? error.message : String(error);
}

function isDirectory(directory) {
  try {
    return fs.statSync(directory).isDirectory();
  } catch {
    return false;
  }
}

const pluginPath = path.join(repoRoot, ".claude-plugin", "plugin.json");
let plugin;

if (!fs.existsSync(pluginPath)) {
  fail(".claude-plugin/plugin.json does not exist.");
} else {
  try {
    plugin = JSON.parse(fs.readFileSync(pluginPath, "utf8"));
  } catch (error) {
    fail(`Could not parse .claude-plugin/plugin.json: ${errorMessage(error)}`);
  }
}

if (!isNonEmptyString(plugin?.name)) {
  fail(".claude-plugin/plugin.json must have a non-empty string name.");
}

if (typeof plugin?.version !== "string") {
  fail(".claude-plugin/plugin.json must have a string version.");
}

if (!Array.isArray(plugin?.skills) || plugin.skills.length === 0) {
  fail(".claude-plugin/plugin.json must have a non-empty skills array.");
}

const skillEntries = Array.isArray(plugin?.skills) ? plugin.skills : [];
const resolvedEntries = [];

for (const skillEntry of skillEntries) {
  if (!isNonEmptyString(skillEntry)) {
    fail("Each .claude-plugin/plugin.json skills entry must be a non-empty string.");
    continue;
  }

  const skillDirectory = path.resolve(repoRoot, skillEntry);

  if (!isWithinDirectory(repoRoot, skillDirectory)) {
    fail(`Skill entry "${skillEntry}" does not resolve to a directory under the repository.`);
    continue;
  }

  if (!isDirectory(skillDirectory)) {
    fail(`Skill entry "${skillEntry}" does not resolve to an existing directory.`);
    continue;
  }

  const skillPath = path.join(skillDirectory, "SKILL.md");

  if (!fs.existsSync(skillPath)) {
    fail(`Skill entry "${skillEntry}" is missing ${relativePath(skillPath)}.`);
    continue;
  }

  resolvedEntries.push({ entry: skillEntry, directory: skillDirectory, skillPath });
}

const seenEntries = new Set();

for (const skillEntry of skillEntries) {
  if (!isNonEmptyString(skillEntry)) {
    continue;
  }

  if (seenEntries.has(skillEntry)) {
    fail(`Duplicate skill entry "${skillEntry}" in .claude-plugin/plugin.json.`);
  }

  seenEntries.add(skillEntry);
}

const entryByDirectory = new Map();

for (const resolvedEntry of resolvedEntries) {
  const priorEntry = entryByDirectory.get(resolvedEntry.directory);

  if (priorEntry && priorEntry !== resolvedEntry.entry) {
    fail(`Duplicate skill entry "${resolvedEntry.entry}" in .claude-plugin/plugin.json.`);
  }

  entryByDirectory.set(resolvedEntry.directory, resolvedEntry.entry);
}

const skillsDirectory = path.join(repoRoot, "skills");
let skillDirectories = [];

if (!isDirectory(skillsDirectory)) {
  fail("Skills directory does not exist or is not a directory.");
} else {
  try {
    skillDirectories = fs.readdirSync(skillsDirectory, { withFileTypes: true }).filter((entry) => entry.isDirectory()).map((entry) => path.join(skillsDirectory, entry.name));
  } catch (error) {
    fail(`Could not read skills: ${errorMessage(error)}`);
  }
}

const listedDirectories = new Set(resolvedEntries.map((entry) => entry.directory));

for (const skillDirectory of skillDirectories) {
  if (!listedDirectories.has(skillDirectory)) {
    fail(`Skill directory "${relativePath(skillDirectory)}" is not listed in .claude-plugin/plugin.json.`);
  }
}

const skillPaths = new Set(resolvedEntries.map((entry) => entry.skillPath));

for (const skillDirectory of skillDirectories) {
  const skillPath = path.join(skillDirectory, "SKILL.md");

  if (fs.existsSync(skillPath)) {
    skillPaths.add(skillPath);
  }
}

const frontmatterByPath = new Map();

for (const skillPath of skillPaths) {
  let contents;

  try {
    contents = fs.readFileSync(skillPath, "utf8");
  } catch (error) {
    fail(`Could not read ${relativePath(skillPath)}: ${errorMessage(error)}`);
    continue;
  }

  const lines = contents.split(/\r?\n/);

  for (const [index, line] of lines.entries()) {
    if (line.includes("!`") && /\$(?:[1-9]|\{[1-9])/.test(line)) {
      fail(`${relativePath(skillPath)}:${index + 1}: Context probe uses a positional parameter; Claude Code replaces $N with an argument before the shell runs, so parse $ARGUMENTS in the Process instead`);
    }
  }

  if (lines[0] !== "---") {
    fail(`${relativePath(skillPath)} must begin with a --- line.`);
    continue;
  }

  const closingIndex = lines.findIndex((line, index) => index > 0 && line === "---");

  if (closingIndex === -1) {
    fail(`${relativePath(skillPath)} is missing a closing --- line.`);
    continue;
  }

  try {
    frontmatterByPath.set(skillPath, load(lines.slice(1, closingIndex).join("\n")));
  } catch (error) {
    fail(`Could not parse YAML frontmatter in ${relativePath(skillPath)}: ${errorMessage(error)}`);
  }
}

for (const [skillPath, frontmatter] of frontmatterByPath) {
  if (frontmatter === null || typeof frontmatter !== "object" || Array.isArray(frontmatter)) {
    fail(`Frontmatter in ${relativePath(skillPath)} must be a mapping.`);
    continue;
  }

  if (!isNonEmptyString(frontmatter.name)) {
    fail(`Frontmatter in ${relativePath(skillPath)} must have a non-empty string name.`);
  } else if (frontmatter.name !== path.basename(path.dirname(skillPath))) {
    fail(`Frontmatter name in ${relativePath(skillPath)} must equal "${path.basename(path.dirname(skillPath))}".`);
  }

  if (!isNonEmptyString(frontmatter.description)) {
    fail(`Frontmatter in ${relativePath(skillPath)} must have a non-empty string description.`);
  }

  if (Object.prototype.hasOwnProperty.call(frontmatter, "argument-hint") && typeof frontmatter["argument-hint"] !== "string") {
    fail(`Frontmatter argument-hint in ${relativePath(skillPath)} must be a string.`);
  }
}

const scriptReference = /\$HOME\/\.agents\/skills\/([a-z0-9-]+)\}\/scripts\/([A-Za-z0-9_.-]+)/g;
const fixedInstallPath = /(?<!\$\{d:-)\$HOME\/\.agents\/skills\//;

for (const skillPath of skillPaths) {
  const contents = fs.readFileSync(skillPath, "utf8");

  if (fixedInstallPath.test(contents)) {
    fail(`${relativePath(skillPath)} names a fixed install path; use the probe form in AUTHORING.md.`);
  }

  for (const match of contents.matchAll(scriptReference)) {
    const scriptPath = path.join(skillsDirectory, match[1], "scripts", match[2]);

    if (!fs.existsSync(scriptPath)) {
      fail(`${relativePath(skillPath)} references ${relativePath(scriptPath)}, which does not exist.`);
    }
  }
}

const identicalCopies = [
  ["skills/use-project-memory/scripts/check.py", "skills/clean-memory/scripts/check.py"],
  ["skills/use-project-memory/scripts/resolve.py", "skills/clean-memory/scripts/resolve.py"],
  ["skills/use-project-memory/references/write.md", "skills/clean-memory/references/write.md"],
  ["skills/distill-session/references/stores.md", "skills/recap-activity/references/stores.md"],
];

for (const [first, second] of identicalCopies) {
  if (!fs.existsSync(path.join(repoRoot, first)) || !fs.existsSync(path.join(repoRoot, second))) {
    fail(`Copies ${first} and ${second} must both exist.`);
  } else if (!fs.readFileSync(path.join(repoRoot, first)).equals(fs.readFileSync(path.join(repoRoot, second)))) {
    fail(`${first} and ${second} must be identical copies.`);
  }
}

const skillNames = [...frontmatterByPath.keys()].map((skillPath) => path.basename(path.dirname(skillPath)));
const requiredBy = new Map();

for (const [skillPath, frontmatter] of frontmatterByPath) {
  const name = path.basename(path.dirname(skillPath));
  const requires = typeof frontmatter?.metadata?.requires === "string" ? frontmatter.metadata.requires.trim().split(/\s+/) : [];
  requiredBy.set(name, requires);

  for (const required of requires) {
    if (required === name || !skillNames.includes(required)) {
      fail(`${relativePath(skillPath)} requires "${required}", which is not another skill here.`);
    }
  }
}

function installedWith(name) {
  const seen = new Set([name]);

  for (const current of seen) {
    for (const required of requiredBy.get(current) ?? []) {
      seen.add(required);
    }
  }

  return seen;
}

function filesIn(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const entryPath = path.join(directory, entry.name);

    if (entry.isDirectory()) {
      return entry.name === "examples" ? [] : filesIn(entryPath);
    }

    return /\.(md|py|mjs|sh)$/.test(entry.name) ? [entryPath] : [];
  });
}

for (const name of skillNames) {
  const available = installedWith(name);

  for (const filePath of filesIn(path.join(skillsDirectory, name))) {
    const contents = fs.readFileSync(filePath, "utf8");

    for (const other of skillNames) {
      if (available.has(other)) {
        continue;
      }

      const readsFile = new RegExp(`(?:\\.\\./|skills/|")${other}(?:/|" /)|(?<![\\w-])${other}/(?:references|scripts|examples)/`);
      const composes = new RegExp(`(?:compos(?:e|ing)|through|delegate to|follow)\\s+\`/?${other}\`(?! when installed)`);

      if (readsFile.test(contents)) {
        fail(`${relativePath(filePath)} reads files of ${other}; add it to metadata.requires or keep a copy.`);
      }

      if (composes.test(contents)) {
        fail(`${relativePath(filePath)} needs ${other}; say what happens without it or add it to metadata.requires.`);
      }
    }
  }
}

const readmePath = path.join(repoRoot, "README.md");
let readme;

if (!fs.existsSync(readmePath)) {
  fail("README.md does not exist.");
} else {
  try {
    readme = fs.readFileSync(readmePath, "utf8");
  } catch (error) {
    fail(`Could not read README.md: ${errorMessage(error)}`);
  }
}

const listedSkillNames = new Set(skillEntries.filter(isNonEmptyString).map((skillEntry) => path.basename(path.resolve(repoRoot, skillEntry))));
const readmeSkillNames = new Set();
let foundSkillsSection = false;

if (typeof readme === "string") {
  let inSkillsSection = false;
  let skillsHeadingLevel = 0;

  for (const line of readme.split(/\r?\n/)) {
    const sectionHeading = line.match(/^(#{1,3})\s+Skills\s*$/);
    const heading = line.match(/^(#{1,6})\s+/);

    if (!inSkillsSection && sectionHeading) {
      foundSkillsSection = true;
      inSkillsSection = true;
      skillsHeadingLevel = sectionHeading[1].length;
      continue;
    }

    if (inSkillsSection && heading && heading[1].length <= skillsHeadingLevel) {
      break;
    }

    if (inSkillsSection) {
      const skillHeading = line.match(/^#### (.+?)\s*$/);

      if (skillHeading) {
        readmeSkillNames.add(skillHeading[1]);
      }
    }
  }
}

if (typeof readme === "string" && !foundSkillsSection) {
  fail("README.md does not contain a Skills section.");
}

for (const skillName of listedSkillNames) {
  if (!readmeSkillNames.has(skillName)) {
    fail(`README.md is missing the heading "#### ${skillName}".`);
  }
}

for (const skillName of readmeSkillNames) {
  if (!listedSkillNames.has(skillName)) {
    fail(`README.md skills heading "#### ${skillName}" does not match a listed skill.`);
  }
}

if (typeof readme === "string") {
  for (const [name, requires] of requiredBy) {
    const entry = readme.split(`#### ${name}\n`)[1]?.split("\n#### ")[0] ?? "";
    const listed = [...(entry.match(/\*\*Requires:\*\*(.*)/)?.[1] ?? "").matchAll(/`([a-z0-9-]+)`/g)].map((match) => match[1]);

    if (listed.join(" ") !== requires.join(" ")) {
      fail(`README.md entry for ${name} must say **Requires:** ${requires.join(", ") || "nothing"}.`);
    }
  }
}

if (errors.length > 0) {
  for (const error of errors) {
    console.error(`ERROR: ${error}`);
  }

  process.exitCode = 1;
} else {
  console.log("All skills validated.");
}
