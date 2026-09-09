import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const excludedDirectories = new Set(["node_modules", ".next", ".git", "dist", "build", "out", "coverage", ".turbo", ".claude"]);
const scannedExtensions = new Set([".tsx", ".jsx", ".ts", ".js", ".css", ".mdx"]);
const sourceExtensions = new Set([".tsx", ".jsx", ".ts", ".js"]);
const maximumFileSize = 2 * 1024 * 1024;

function errorMessage(error) {
  return error instanceof Error ? error.message : String(error);
}

function normalizePath(filePath) {
  return filePath.split(path.sep).join("/");
}

function relativePath(appPath, filePath) {
  return normalizePath(path.relative(appPath, filePath));
}

function isDirectory(directory) {
  try {
    return fs.statSync(directory).isDirectory();
  } catch {
    return false;
  }
}

function isWithinDirectory(directory, candidate) {
  const relative = path.relative(directory, candidate);
  return relative.length > 0 && relative !== ".." && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative);
}

function walkFiles(appPath) {
  const files = [];
  const componentDirectories = [];

  function walk(directory) {
    const directoryName = path.basename(directory).toLowerCase();

    if (directoryName === "ui" || directoryName === "shared" || directoryName === "charts") {
      componentDirectories.push(directory);
    }

    const entries = fs.readdirSync(directory, { withFileTypes: true }).sort((left, right) => left.name.localeCompare(right.name));

    for (const entry of entries) {
      const entryPath = path.join(directory, entry.name);

      if (entry.isSymbolicLink()) {
        continue;
      }

      if (entry.isDirectory()) {
        if (!excludedDirectories.has(entry.name)) {
          walk(entryPath);
        }

        continue;
      }

      if (!entry.isFile() || !scannedExtensions.has(path.extname(entry.name))) {
        continue;
      }

      if (fs.statSync(entryPath).size <= maximumFileSize) {
        files.push(entryPath);
      }
    }
  }

  if (!isDirectory(appPath)) {
    throw new Error(`App path is not a directory: ${appPath}`);
  }

  walk(appPath);
  return { files, componentDirectories };
}

function createCounter() {
  return new Map();
}

function addCount(counter, value, filePath, amount = 1) {
  let files = counter.get(value);

  if (!files) {
    files = new Map();
    counter.set(value, files);
  }

  files.set(filePath, (files.get(filePath) ?? 0) + amount);
}

function totalCount(files) {
  return [...files.values()].reduce((total, count) => total + count, 0);
}

function topFiles(files) {
  return [...files.entries()]
    .map(([file, count]) => ({ file, count }))
    .sort((left, right) => right.count - left.count || left.file.localeCompare(right.file))
    .slice(0, 3);
}

function counterData(counter) {
  return Object.fromEntries(
    [...counter.entries()]
      .map(([value, files]) => ({ value, count: totalCount(files), topFiles: topFiles(files) }))
      .sort((left, right) => right.count - left.count || left.value.localeCompare(right.value))
      .map(({ value, count, topFiles: files }) => [value, { count, topFiles: files }]),
  );
}

function countMatches(contents, expression) {
  const matches = contents.match(expression);
  return matches ? matches.length : 0;
}

function skipQuoted(contents, index, quote) {
  let current = index + 1;

  while (current < contents.length) {
    if (contents[current] === "\\") {
      current += 2;
    } else if (contents[current] === quote) {
      return current + 1;
    } else {
      current += 1;
    }
  }

  return current;
}

function skipLineComment(contents, index) {
  const newline = contents.indexOf("\n", index + 2);
  return newline === -1 ? contents.length : newline + 1;
}

function skipBlockComment(contents, index) {
  const closing = contents.indexOf("*/", index + 2);
  return closing === -1 ? contents.length : closing + 2;
}

function skipTemplate(contents, index) {
  let current = index + 1;

  while (current < contents.length) {
    if (contents[current] === "\\") {
      current += 2;
    } else if (contents[current] === "`") {
      return current + 1;
    } else if (contents[current] === "$" && contents[current + 1] === "{") {
      current = skipTemplateExpression(contents, current + 2);
    } else {
      current += 1;
    }
  }

  return current;
}

function skipTemplateExpression(contents, index) {
  let current = index;
  let depth = 1;

  while (current < contents.length && depth > 0) {
    const character = contents[current];

    if (character === "\"" || character === "'") {
      current = skipQuoted(contents, current, character);
    } else if (character === "`") {
      current = skipTemplate(contents, current);
    } else if (character === "/" && contents[current + 1] === "/") {
      current = skipLineComment(contents, current);
    } else if (character === "/" && contents[current + 1] === "*") {
      current = skipBlockComment(contents, current);
    } else if (character === "{") {
      depth += 1;
      current += 1;
    } else if (character === "}") {
      depth -= 1;
      current += 1;
    } else {
      current += 1;
    }
  }

  return current;
}

function readQuoted(contents, index, quote) {
  let current = index + 1;
  let value = "";

  while (current < contents.length) {
    const character = contents[current];

    if (character === "\\") {
      if (current + 1 < contents.length) {
        value += contents[current + 1];
      }

      current += 2;
    } else if (character === quote) {
      return { value, nextIndex: current + 1 };
    } else {
      value += character;
      current += 1;
    }
  }

  return { value, nextIndex: current };
}

function readTemplate(contents, index) {
  let current = index + 1;
  let value = "";

  while (current < contents.length) {
    const character = contents[current];

    if (character === "\\") {
      if (current + 1 < contents.length) {
        value += contents[current + 1];
      }

      current += 2;
    } else if (character === "`") {
      return { value, nextIndex: current + 1 };
    } else if (character === "$" && contents[current + 1] === "{") {
      value += " ";
      current = skipTemplateExpression(contents, current + 2);
    } else {
      value += character;
      current += 1;
    }
  }

  return { value, nextIndex: current };
}

function stringLiterals(contents) {
  const literals = [];
  let index = 0;

  while (index < contents.length) {
    const character = contents[index];

    if (character === "/" && contents[index + 1] === "/") {
      index = skipLineComment(contents, index);
    } else if (character === "/" && contents[index + 1] === "*") {
      index = skipBlockComment(contents, index);
    } else if (character === "\"" || character === "'") {
      const literal = readQuoted(contents, index, character);
      literals.push(literal.value);
      index = literal.nextIndex;
    } else if (character === "`") {
      const literal = readTemplate(contents, index);
      literals.push(literal.value);
      index = literal.nextIndex;
    } else {
      index += 1;
    }
  }

  return literals;
}

function splitTokens(value) {
  return value
    .split(/\s+/)
    .map((token) => token.replace(/[;,]+$/g, ""))
    .filter(Boolean);
}

function stripVariantPrefix(token) {
  let value = token;

  while (value) {
    let depth = 0;
    let separator = -1;

    for (let index = 0; index < value.length; index += 1) {
      if (value[index] === "[") {
        depth += 1;
      } else if (value[index] === "]") {
        depth = Math.max(0, depth - 1);
      } else if (value[index] === ":" && depth === 0) {
        separator = index;
        break;
      }
    }

    if (separator === -1 || separator === 0) {
      return value;
    }

    value = value.slice(separator + 1);
  }

  return value;
}

function isPanelSurface(token) {
  return /^(?:bg-(?:muted|card|accent)|border)(?:\/[^\s]+)?$/.test(token);
}

function importsRecharts(contents) {
  return /(?:^|[;\n])\s*import(?:\s+type)?(?:[\s\S]*?\s+from)?\s*["']recharts["']/.test(contents) || /\bimport\s*\(\s*["']recharts["']\s*\)/.test(contents);
}

function hasEntranceAnimationOff(contents) {
  return /isAnimationActive\s*=\s*\{\s*false\s*\}/.test(contents);
}

function firstRootValue(contents) {
  const match = contents.match(/(?:html\s*\{[^}]*?font-size:\s*([^;}]+)|body\s*\{[^}]*?font-size:\s*([^;}]+)|--text-base:\s*([^;}]+))/);
  return match ? (match[1] ?? match[2] ?? match[3]).trim() : undefined;
}

function firstCssValue(contents, name) {
  const match = contents.match(new RegExp(`--${name}:\\s*([^;}]+)`));
  return match ? match[1].trim() : undefined;
}

function cssValues(contents, name) {
  return [...contents.matchAll(new RegExp(`--${name}:\\s*([^;}]+)`, "g"))].map((match) => match[1].trim());
}

function componentData(componentDirectories, files, appPath) {
  return Object.fromEntries(
    [...new Set(componentDirectories)]
      .sort((left, right) => relativePath(appPath, left).localeCompare(relativePath(appPath, right)))
      .map((directory) => {
        const names = files
          .filter((filePath) => path.extname(filePath) === ".tsx" && isWithinDirectory(directory, filePath))
          .map((filePath) => path.basename(filePath, ".tsx"))
          .sort((left, right) => left.localeCompare(right));
        return [relativePath(appPath, directory), names];
      }),
  );
}

function createAudit(appArgument) {
  const appPath = path.resolve(appArgument);
  const { files, componentDirectories } = walkFiles(appPath);
  const typeClasses = createCounter();
  const radiusClasses = createCounter();
  const controlsClasses = createCounter();
  const rowClasses = createCounter();
  const handStyledPanels = createCounter();
  const cardTags = createCounter();
  const shadowClasses = createCounter();
  const maxWidths = createCounter();
  const sidebarWidths = createCounter();
  const ruleClasses = createCounter();
  const pillClasses = createCounter();
  const motionClasses = createCounter();
  const rechartsFileCounts = createCounter();
  const entranceOffFileCounts = createCounter();
  const routeFiles = {
    page: createCounter(),
    layout: createCounter(),
    loading: createCounter(),
    error: createCounter(),
  };
  let root;
  let rootFile;
  let radiusToken;
  let radiusTokenFile;
  let rechartsFiles = 0;
  let entranceOff = 0;

  for (const filePath of files) {
    const contents = fs.readFileSync(filePath, "utf8");
    const file = relativePath(appPath, filePath);
    const extension = path.extname(filePath);
    const basename = path.basename(filePath).toLowerCase();
    const isSidebarFile = basename.includes("sidebar");

    if (isSidebarFile) {
      for (const match of contents.matchAll(/SIDEBAR_WIDTH\s*=\s*"([^"]+)"/g)) {
        addCount(sidebarWidths, match[1], file);
      }
    }

    if (path.basename(filePath) === "page.tsx") {
      addCount(routeFiles.page, "page", file);
    } else if (path.basename(filePath) === "layout.tsx") {
      addCount(routeFiles.layout, "layout", file);
    } else if (path.basename(filePath) === "loading.tsx") {
      addCount(routeFiles.loading, "loading", file);
    } else if (path.basename(filePath) === "error.tsx") {
      addCount(routeFiles.error, "error", file);
    }

    if (countMatches(contents, /<Card\b/g) > 0) {
      addCount(cardTags, "Card tags", file, countMatches(contents, /<Card\b/g));
    }

    if (sourceExtensions.has(extension)) {
      if (importsRecharts(contents)) {
        rechartsFiles += 1;
        addCount(rechartsFileCounts, "recharts files", file);

        if (hasEntranceAnimationOff(contents)) {
          entranceOff += 1;
          addCount(entranceOffFileCounts, "with entrance animation off", file);
        }
      }

      for (const literal of stringLiterals(contents)) {
        const tokens = splitTokens(literal);
        const classTokens = tokens.map(stripVariantPrefix);

        if (classTokens.some((token) => /^rounded-(?:lg|xl|2xl|3xl)$/.test(token)) && classTokens.some(isPanelSurface)) {
          addCount(handStyledPanels, "Hand styled", file);
        }

        for (const token of classTokens) {
          if (/^text-(?:xs|sm|base|lg|xl|2xl|3xl|4xl|5xl)$/.test(token) || /^text-\[\d+px\]$/.test(token)) {
            addCount(typeClasses, token, file);
          }

          if (token === "rounded" || /^rounded-(?:none|sm|md|lg|xl|2xl|3xl|full)$/.test(token) || /^rounded-\[[^\]]+\]$/.test(token)) {
            addCount(radiusClasses, token, file);
          }

          if (/^h-(?:6|7|8|9|10|11|12)$/.test(token) || /^h-\[\d+px\]$/.test(token) || /^size-(?:6|7|8|9|10|11|12)$/.test(token)) {
            addCount(controlsClasses, token, file);
          }

          if (/^py-(?:1|1\.5|2|2\.5|3|4)$/.test(token) || /^p-(?:2|3|4|5|6)$/.test(token)) {
            addCount(rowClasses, token, file);
          }

          if (token === "shadow" || /^shadow-(?:xs|sm|md|lg|xl|2xl)$/.test(token)) {
            addCount(shadowClasses, token, file);
          }

          if (/^max-w-.+$/.test(token)) {
            addCount(maxWidths, token, file);
          }

          if (isSidebarFile && (token === "w-64" || /^w-\[\d{3,}px\]$/.test(token))) {
            addCount(sidebarWidths, token, file);
          }

          if (token === "border" || /^border-(?:t|b|l|r|x|y)(?:-.+)?$/.test(token) || /^divide-(?:x|y)(?:-.+)?$/.test(token)) {
            addCount(ruleClasses, token, file);
          }

          if ((basename.includes("badge") || basename.includes("chip") || basename.includes("tag") || basename.includes("pill")) && token === "rounded-full") {
            addCount(pillClasses, token, file);
          }

          if (token === "transition-all" || /^animate-.+$/.test(token)) {
            addCount(motionClasses, token, file);
          }
        }
      }
    }

    if (extension === ".css") {
      const css = contents.replace(/\/\*[\s\S]*?\*\//g, "");

      if (root === undefined) {
        const value = firstRootValue(css);

        if (value !== undefined) {
          root = value;
          rootFile = file;
        }
      }

      if (radiusToken === undefined) {
        const value = firstCssValue(css, "radius");

        if (value !== undefined) {
          radiusToken = value;
          radiusTokenFile = file;
        }
      }

      for (const value of cssValues(css, "sidebar-width")) {
        addCount(sidebarWidths, value, file);
      }

      for (const line of css.split(/\r?\n/)) {
        for (const match of line.matchAll(/@apply\s+([^;]+)/g)) {
          for (const token of splitTokens(match[1]).map(stripVariantPrefix)) {
            if (/^text-(?:xs|sm|base|lg|xl|2xl|3xl|4xl|5xl)$/.test(token) || /^text-\[\d+px\]$/.test(token)) {
              addCount(typeClasses, token, file);
            }

            if (token === "rounded" || /^rounded-(?:none|sm|md|lg|xl|2xl|3xl|full)$/.test(token) || /^rounded-\[[^\]]+\]$/.test(token)) {
              addCount(radiusClasses, token, file);
            }

            if (/^h-(?:6|7|8|9|10|11|12)$/.test(token) || /^h-\[\d+px\]$/.test(token) || /^size-(?:6|7|8|9|10|11|12)$/.test(token)) {
              addCount(controlsClasses, token, file);
            }

            if (/^py-(?:1|1\.5|2|2\.5|3|4)$/.test(token) || /^p-(?:2|3|4|5|6)$/.test(token)) {
              addCount(rowClasses, token, file);
            }

            if (token === "shadow" || /^shadow-(?:xs|sm|md|lg|xl|2xl)$/.test(token)) {
              addCount(shadowClasses, token, file);
            }

            if (/^max-w-.+$/.test(token)) {
              addCount(maxWidths, token, file);
            }

            if (isSidebarFile && (token === "w-64" || /^w-\[\d{3,}px\]$/.test(token))) {
              addCount(sidebarWidths, token, file);
            }

            if (token === "border" || /^border-(?:t|b|l|r|x|y)(?:-.+)?$/.test(token) || /^divide-(?:x|y)(?:-.+)?$/.test(token)) {
              addCount(ruleClasses, token, file);
            }

            if ((basename.includes("badge") || basename.includes("chip") || basename.includes("tag") || basename.includes("pill")) && token === "rounded-full") {
              addCount(pillClasses, token, file);
            }

            if (token === "transition-all" || /^animate-.+$/.test(token)) {
              addCount(motionClasses, token, file);
            }
          }
        }
      }
    }
  }

  const dimensions = {
    type: { classes: counterData(typeClasses), root: root ?? "(not set)" },
    radius: { classes: counterData(radiusClasses), token: radiusToken ?? "(not set)" },
    controls: { classes: counterData(controlsClasses) },
    rows: { classes: counterData(rowClasses) },
    panels: { handStyled: totalCount(handStyledPanels.get("Hand styled") ?? new Map()), cardTags: totalCount(cardTags.get("Card tags") ?? new Map()), topFiles: topFiles(handStyledPanels.get("Hand styled") ?? new Map()) },
    shadows: { classes: counterData(shadowClasses) },
    widths: { maxWidths: counterData(maxWidths), sidebar: counterData(sidebarWidths) },
    rules: { classes: counterData(ruleClasses) },
    pills: { count: totalCount(pillClasses.get("rounded-full") ?? new Map()), topFiles: topFiles(pillClasses.get("rounded-full") ?? new Map()) },
    motion: { classes: counterData(motionClasses), rechartsFiles, entranceOff },
  };
  const routes = Object.fromEntries(Object.entries(routeFiles).map(([name, filesByRoute]) => [name, totalCount(filesByRoute.get(name) ?? new Map())]));

  return {
    json: {
      app: appArgument,
      files: files.length,
      dimensions,
      components: componentData(componentDirectories, files, appPath),
      routes,
    },
    details: {
      appPath,
      rootFile,
      radiusTokenFile,
      cardTagFiles: topFiles(cardTags.get("Card tags") ?? new Map()),
      rechartsFiles: topFiles(rechartsFileCounts.get("recharts files") ?? new Map()),
      entranceOffFiles: topFiles(entranceOffFileCounts.get("with entrance animation off") ?? new Map()),
      routeFiles: Object.fromEntries(Object.entries(routeFiles).map(([name, filesByRoute]) => [name, topFiles(filesByRoute.get(name) ?? new Map())])),
    },
  };
}

function formatTopFiles(files) {
  return files.length > 0 ? files.map(({ file, count }) => `${file} ${count}`).join(", ") : "(none)";
}

function escapeCell(value) {
  return String(value).replace(/\|/g, "\\|").replace(/\r?\n/g, " ");
}

function classRows(rows, dimension, classes) {
  for (const [value, data] of Object.entries(classes)) {
    rows.push([dimension, value, data.count, formatTopFiles(data.topFiles)]);
  }
}

function formatMarkdown(audit) {
  const { json, details } = audit;
  const rows = [];

  classRows(rows, "Type", json.dimensions.type.classes);
  rows.push(["Type", `root: ${json.dimensions.type.root}`, details.rootFile ? 1 : 0, details.rootFile ? `${details.rootFile} 1` : "(none)"]);
  classRows(rows, "Radius", json.dimensions.radius.classes);
  rows.push(["Radius", `token: ${json.dimensions.radius.token}`, details.radiusTokenFile ? 1 : 0, details.radiusTokenFile ? `${details.radiusTokenFile} 1` : "(none)"]);
  classRows(rows, "Controls", json.dimensions.controls.classes);
  classRows(rows, "Rows", json.dimensions.rows.classes);
  rows.push(["Panels", "hand styled", json.dimensions.panels.handStyled, formatTopFiles(json.dimensions.panels.topFiles)]);
  rows.push(["Panels", "Card tags", json.dimensions.panels.cardTags, formatTopFiles(details.cardTagFiles)]);
  classRows(rows, "Shadows", json.dimensions.shadows.classes);
  classRows(rows, "Widths", json.dimensions.widths.maxWidths);
  const sidebarEntries = Object.entries(json.dimensions.widths.sidebar);

  if (sidebarEntries.length === 0) {
    rows.push(["Widths", "sidebar: (not set)", 0, "(none)"]);
  } else {
    for (const [value, data] of sidebarEntries) {
      rows.push(["Widths", `sidebar: ${value}`, data.count, formatTopFiles(data.topFiles)]);
    }
  }

  classRows(rows, "Rules", json.dimensions.rules.classes);
  rows.push(["Pills", "rounded-full", json.dimensions.pills.count, formatTopFiles(json.dimensions.pills.topFiles)]);
  classRows(rows, "Motion", json.dimensions.motion.classes);
  rows.push(["Motion", "recharts files", json.dimensions.motion.rechartsFiles, formatTopFiles(details.rechartsFiles)]);
  rows.push(["Motion", "with entrance animation off", json.dimensions.motion.entranceOff, formatTopFiles(details.entranceOffFiles)]);

  for (const [directory, names] of Object.entries(json.components)) {
    const files = names.map((name) => ({ file: `${directory}/${name}.tsx`, count: 1 }));
    rows.push(["Components", `${directory}: ${names.join(" ") || "(none)"}`, names.length, formatTopFiles(files)]);
  }

  for (const name of ["page", "layout", "loading", "error"]) {
    rows.push(["Routes", name, json.routes[name], formatTopFiles(details.routeFiles[name])]);
  }

  return [
    `Density audit of ${json.app} (${json.files} files scanned)`,
    "",
    "| Dimension | Value | Count | Top files |",
    "| --- | --- | ---: | --- |",
    ...rows.map((row) => `| ${row.map(escapeCell).join(" | ")} |`),
  ].join("\n");
}

function classCount(classes, name) {
  return classes[name]?.count ?? 0;
}

function formatValue(value) {
  const formatted = JSON.stringify(value);
  return formatted === undefined ? String(value) : formatted;
}

function assertEqual(label, actual, expected) {
  if (JSON.stringify(actual) === JSON.stringify(expected)) {
    console.log(`${label} ok`);
    return true;
  }

  console.error(`${label}: expected ${formatValue(expected)}, received ${formatValue(actual)}.`);
  return false;
}

function assertCondition(label, actual, expected) {
  if (actual) {
    console.log(`${label} ok`);
    return true;
  }

  console.error(`${label}: expected ${expected}, received ${formatValue(actual)}.`);
  return false;
}

function writeFixtureFile(fixture, relative, contents) {
  const filePath = path.join(fixture, relative);
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, contents, "utf8");
}

function runSelfTest() {
  let fixture;
  let passed = false;

  try {
    fixture = fs.mkdtempSync(path.join(os.tmpdir(), "density-"));
    writeFixtureFile(fixture, "components/ui/card.tsx", "const classes = \"rounded-xl bg-muted/50 border shadow-sm p-6 text-base transition-all\";\nconst card = <Card />;\n");
    writeFixtureFile(fixture, "components/ui/badge.tsx", "const classes = \"rounded-full text-xs\";\n");
    writeFixtureFile(fixture, "app/page.tsx", "import { BarChart } from \"recharts\";\nconst classes = \"max-w-6xl h-9 py-3 border-b divide-y text-sm\";\n");
    writeFixtureFile(fixture, "components/shared/sidebar.tsx", "const classes = \"w-64\";\n");
    writeFixtureFile(fixture, "styles/globals.css", "html { font-size: 16px; }\n:root { --radius: 0.875rem; --sidebar-width: 16rem; }\n");

    const audit = createAudit(fixture).json;
    const checks = [
      assertEqual("type text-base", classCount(audit.dimensions.type.classes, "text-base"), 1),
      assertEqual("type text-xs", classCount(audit.dimensions.type.classes, "text-xs"), 1),
      assertEqual("type text-sm", classCount(audit.dimensions.type.classes, "text-sm"), 1),
      assertEqual("type root", audit.dimensions.type.root, "16px"),
      assertEqual("radius rounded-xl", classCount(audit.dimensions.radius.classes, "rounded-xl"), 1),
      assertEqual("radius rounded-full", classCount(audit.dimensions.radius.classes, "rounded-full"), 1),
      assertEqual("radius token", audit.dimensions.radius.token, "0.875rem"),
      assertEqual("controls h-9", classCount(audit.dimensions.controls.classes, "h-9"), 1),
      assertEqual("rows p-6", classCount(audit.dimensions.rows.classes, "p-6"), 1),
      assertEqual("rows py-3", classCount(audit.dimensions.rows.classes, "py-3"), 1),
      assertEqual("panels hand styled", audit.dimensions.panels.handStyled, 1),
      assertEqual("panels Card tags", audit.dimensions.panels.cardTags, 1),
      assertEqual("shadows shadow-sm", classCount(audit.dimensions.shadows.classes, "shadow-sm"), 1),
      assertEqual("widths max-w-6xl", classCount(audit.dimensions.widths.maxWidths, "max-w-6xl"), 1),
      assertCondition("widths sidebar", Object.hasOwn(audit.dimensions.widths.sidebar, "w-64") && Object.hasOwn(audit.dimensions.widths.sidebar, "16rem"), "both w-64 and 16rem"),
      assertEqual("rules border-b", classCount(audit.dimensions.rules.classes, "border-b"), 1),
      assertEqual("rules divide-y", classCount(audit.dimensions.rules.classes, "divide-y"), 1),
      assertEqual("pills", audit.dimensions.pills.count, 1),
      assertEqual("motion transition-all", classCount(audit.dimensions.motion.classes, "transition-all"), 1),
      assertEqual("motion recharts files", audit.dimensions.motion.rechartsFiles, 1),
      assertEqual("motion with entrance animation off", audit.dimensions.motion.entranceOff, 0),
      assertEqual("components ui", audit.components["components/ui"], ["badge", "card"]),
      assertEqual("components shared", audit.components["components/shared"], ["sidebar"]),
      assertEqual("routes page", audit.routes.page, 1),
      assertEqual("routes layout", audit.routes.layout, 0),
    ];

    passed = checks.every(Boolean);

    if (passed) {
      console.log("self-test ok");
    }
  } catch (error) {
    console.error(`Self-test failed: ${errorMessage(error)}`);
    passed = false;
  } finally {
    if (fixture) {
      try {
        fs.rmSync(fixture, { recursive: true, force: true });
      } catch (error) {
        console.error(`Self-test cleanup failed: ${errorMessage(error)}`);
        passed = false;
      }
    }
  }

  return passed;
}

function printUsage() {
  console.error("Usage: node density.mjs <app-path> [--json] | node density.mjs --self-test");
}

function main() {
  const argumentsList = process.argv.slice(2);

  if (argumentsList.length === 1 && argumentsList[0] === "--self-test") {
    process.exitCode = runSelfTest() ? 0 : 1;
    return;
  }

  let appArgument;
  let json = false;

  for (const argument of argumentsList) {
    if (argument === "--json") {
      json = true;
    } else if (!argument.startsWith("-") && appArgument === undefined) {
      appArgument = argument;
    } else {
      printUsage();
      process.exitCode = 2;
      return;
    }
  }

  if (appArgument === undefined) {
    printUsage();
    process.exitCode = 2;
    return;
  }

  try {
    const audit = createAudit(appArgument);
    console.log(json ? JSON.stringify(audit.json, null, 2) : formatMarkdown(audit));
  } catch (error) {
    console.error(`Error: ${errorMessage(error)}`);
    process.exitCode = 1;
  }
}

main();
