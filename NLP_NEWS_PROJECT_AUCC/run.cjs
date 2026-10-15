const { spawn, spawnSync } = require('node:child_process');
const { existsSync } = require('node:fs');
const path = require('node:path');
const net = require('node:net');

const root = __dirname;
const python = path.join(root, 'backend', 'venv', 'Scripts', 'python.exe');
const vite = path.join(root, 'frontend', 'node_modules', 'vite', 'bin', 'vite.js');
const online = process.argv.includes('--cloudflare');
const children = new Set();
let stopping = false;

function stop(code = 0) {
  if (stopping) return;
  stopping = true;
  process.exitCode = code;
  console.log('\nStopping services...');
  for (const child of children) {
    if (child.exitCode !== null || !child.pid) continue;
    // Kill only process trees created by this launcher, including venv Python.
    spawnSync('taskkill', ['/pid', String(child.pid), '/T', '/F'], {
      windowsHide: true, stdio: 'ignore',
    });
  }
}

function launch(name, command, args, directory) {
  const child = spawn(command, args, {
    cwd: path.join(root, directory), windowsHide: true,
    stdio: ['ignore', 'pipe', 'pipe'],
    env: { ...process.env, PYTHONUNBUFFERED: '1' },
  });
  children.add(child);
  child.stdout.on('data', data => process.stdout.write(data));
  child.stderr.on('data', data => process.stderr.write(data));
  child.on('error', error => {
    console.error(`${name}: ${error.message}`);
    stop(1);
  });
  child.on('exit', code => {
    children.delete(child);
    if (!stopping) {
      console.error(`${name} stopped (exit ${code}).`);
      stop(code || 1);
    }
  });
}

function checkPort(port) {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.once('error', () => reject(new Error(
      `Port ${port} is busy. Stop the previous backend/frontend first, then run again.`
    )));
    server.listen(port, '127.0.0.1', () => server.close(resolve));
  });
}

async function main() {
  if (!existsSync(python)) throw new Error('Python environment missing. See run-cloudflare.txt for setup.');
  if (!existsSync(vite)) throw new Error('Run npm.cmd install in frontend first.');
  let tunnel;
  if (online) {
    const located = spawnSync('where.exe', ['cloudflared.exe'], { encoding: 'utf8', windowsHide: true });
    tunnel = [
      ...(located.stdout || '').trim().split(/\r?\n/),
      path.join(process.env['ProgramFiles(x86)'] || '', 'cloudflared', 'cloudflared.exe'),
      path.join(process.env.ProgramFiles || '', 'cloudflared', 'cloudflared.exe'),
    ].find(candidate => candidate && existsSync(candidate));
    if (!tunnel) throw new Error('cloudflared.exe not found. Install Cloudflare Tunnel first.');
  }
  if (process.argv.includes('--check')) {
    console.log('Launcher prerequisites OK.');
    return;
  }
  await Promise.all([checkPort(8000), checkPort(5173)]);
  process.on('SIGINT', () => stop());
  process.on('SIGTERM', () => stop());
  console.log('Website: http://127.0.0.1:5173\nLogs appear here. Press Ctrl+C to stop all services.');
  launch('Backend', python, ['-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000'], 'backend');
  launch('Frontend', process.execPath, [vite, '--host', '127.0.0.1', '--port', '5173', '--strictPort', '--open'], 'frontend');
  if (online) {
    console.log('Share the https://....trycloudflare.com URL printed below once services are ready.');
    launch('Cloudflare', tunnel, ['tunnel', '--url', 'http://127.0.0.1:5173', '--protocol', 'http2'], '.');
  }
}

main().catch(error => {
  console.error(error.message);
  process.exitCode = 1;
});
