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

if (errors.length > 0) {
  for (const error of errors) {
    console.error(`ERROR: ${error}`);
  }

  process.exitCode = 1;
} else {
  console.log("All skills validated.");
}
