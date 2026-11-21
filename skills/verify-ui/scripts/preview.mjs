#!/usr/bin/env node
// Serves a production build, and this skill's detail audit, from a local port with CORS headers, so a page the user
// is signed in to can load the new build against its real API, and any page can load the audit.
// Usage: node preview.mjs <build-dir> [port]   (build the app with its asset base set to http://localhost:<port>/ first)
import { createServer } from 'node:http';
import { readFile, realpath } from 'node:fs/promises';
import { dirname, extname, join, normalize, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

if (!process.argv[2]) {
  console.error('usage: node preview.mjs <build-dir> [port]');
  process.exit(1);
}
const root = await realpath(resolve(process.argv[2]));
const port = Number(process.argv[3] ?? 4173);
const audit = join(dirname(fileURLToPath(import.meta.url)), 'detail-audit.js');
const types = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.mjs': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.map': 'application/json',
  '.webmanifest': 'application/manifest+json',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.wasm': 'application/wasm',
};
const cors = {
  'access-control-allow-origin': '*',
  'access-control-allow-methods': 'GET, OPTIONS',
  'access-control-allow-headers': '*',
  'access-control-allow-private-network': 'true',
};

createServer(async (request, response) => {
  if (request.method === 'OPTIONS') {
    response.writeHead(204, cors);
    response.end();
    return;
  }
  try {
    const path = normalize(decodeURIComponent(new URL(request.url, 'http://x').pathname));
    let file = audit;
    if (path !== '/__audit.js') {
      file = await realpath(join(root, path === '/' ? 'index.html' : path));
      if (file !== root && !file.startsWith(root + sep)) throw new Error('outside the build');
    }
    const body = await readFile(file);
    response.writeHead(200, { ...cors, 'content-type': types[extname(file)] ?? 'application/octet-stream', 'cache-control': 'no-store' });
    response.end(body);
  } catch {
    response.writeHead(404, cors);
    response.end();
  }
}).listen(port, '127.0.0.1', () => {
  const base = `http://localhost:${port}`;
  console.log(`serving ${root} on ${base}`);
  console.log('load the build into the signed in page (reload it first for every new build):');
  console.log(`  const html = await (await fetch('${base}/index.html', { cache: 'no-store' })).text(); document.open(); document.write(html); document.close();`);
  console.log("run the detail audit in any page (where the page's CSP blocks eval, paste the file's contents into the script runner instead):");
  console.log(`  const src = await (await fetch('${base}/__audit.js', { cache: 'no-store' })).text(); return await new Function('return ' + src.replace(/^\\/\\/.*$/gm, '').trim().replace(/;\\s*$/, ''))();`);
});
