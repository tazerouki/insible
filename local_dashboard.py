import http.server
import socketserver
import json
import os
import urllib.parse

PORT = 8088
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Semaphore UI - Local Test Environment</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --semaphore-sidebar: #0f3e47;
            --semaphore-sidebar-active: #175460;
            --semaphore-bg: #f8fafc;
        }
        body {
            background-color: var(--semaphore-bg);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #334155;
            height: 100vh;
            overflow: hidden;
        }
        .sidebar {
            background-color: var(--semaphore-sidebar);
            color: #e2e8f0;
            min-height: 100vh;
            width: 240px;
            flex-shrink: 0;
        }
        .project-select {
            padding: 16px;
            font-weight: 700;
            font-size: 1.1rem;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .nav-link-custom {
            display: flex;
            align-items: center;
            padding: 12px 20px;
            color: #cbd5e1;
            text-decoration: none;
            font-size: 0.95rem;
            font-weight: 500;
            transition: all 0.15s ease;
        }
        .nav-link-custom:hover {
            background-color: rgba(255,255,255,0.05);
            color: #ffffff;
        }
        .nav-link-custom.active {
            background-color: var(--semaphore-sidebar-active);
            color: #ffffff;
            font-weight: 600;
        }
        .nav-link-custom i {
            margin-right: 12px;
            width: 18px;
            text-align: center;
        }
        .main-content {
            flex-grow: 1;
            overflow-y: auto;
            padding: 30px 40px;
        }
        .page-title {
            font-size: 1.5rem;
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 24px;
        }
        .tab-menu {
            border-bottom: 2px solid #e2e8f0;
            margin-bottom: 24px;
            display: flex;
            gap: 24px;
        }
        .tab-item {
            padding-bottom: 10px;
            font-weight: 600;
            color: #64748b;
            cursor: pointer;
            border-bottom: 2px solid transparent;
            margin-bottom: -2px;
        }
        .tab-item.active {
            color: #2563eb;
            border-bottom-color: #2563eb;
        }
        .table-custom {
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            border: 1px solid #e2e8f0;
        }
        .table-custom th {
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            color: #64748b;
            font-weight: 700;
            padding: 16px 20px;
            border-bottom: 1px solid #e2e8f0;
        }
        .table-custom td {
            padding: 16px 20px;
            vertical-align: middle;
            border-bottom: 1px solid #f1f5f9;
            font-size: 0.9rem;
        }
        .badge-success-custom {
            background-color: #22c55e;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.8rem;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .btn-run {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background-color: #f1f5f9;
            border: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: #334155;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-run:hover {
            background-color: #22c55e;
            color: white;
        }
        .playbook-link {
            color: #2563eb;
            text-decoration: none;
            font-weight: 600;
            cursor: pointer;
        }
        .playbook-link:hover {
            text-decoration: underline;
        }
        .modal-code {
            background-color: #1e1e1e;
            color: #d4d4d4;
            font-family: 'Consolas', monospace;
            padding: 15px;
            border-radius: 6px;
            max-height: 450px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>

<div class="d-flex">
    <!-- Sidebar -->
    <div class="sidebar">
        <div class="project-select">
            <span>Remote Instal...<br><small style="font-weight:400; font-size:0.8rem; opacity:0.8;">manager</small></span>
            <i class="fa-solid fa-chevron-down" style="font-size:0.8rem;"></i>
        </div>
        <div class="pt-3">
            <a href="#" class="nav-link-custom" onclick="showSection('dashboard', this)">
                <i class="fa-solid fa-chart-pie"></i> Dashboard
            </a>
            <a href="#" class="nav-link-custom active" onclick="showSection('templates', this)">
                <i class="fa-solid fa-bars-progress"></i> Task Templates
            </a>
            <a href="#" class="nav-link-custom" onclick="showSection('schedule', this)">
                <i class="fa-regular fa-clock"></i> Schedule
            </a>
            <a href="#" class="nav-link-custom" onclick="showSection('inventory', this)">
                <i class="fa-solid fa-server"></i> Inventory
            </a>
            <a href="#" class="nav-link-custom" onclick="showSection('variables', this)">
                <i class="fa-solid fa-layer-group"></i> Variable Groups
            </a>
            <a href="#" class="nav-link-custom" onclick="showSection('keystore', this)">
                <i class="fa-solid fa-key"></i> Key Store
            </a>
            <a href="#" class="nav-link-custom" onclick="showSection('repositories', this)">
                <i class="fa-solid fa-code-branch"></i> Repositories
            </a>
            <a href="#" class="nav-link-custom" onclick="showSection('integrations', this)">
                <i class="fa-solid fa-plug"></i> Integrations
            </a>
            <a href="#" class="nav-link-custom" onclick="showSection('team', this)">
                <i class="fa-solid fa-users"></i> Team
            </a>
        </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
        <!-- Section: Task Templates -->
        <div id="section-templates">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h1 class="page-title mb-0">Task Templates</h1>
                <button class="btn btn-primary" onclick="alert('Création de template en mode simulation local.')"><i class="fa-solid fa-plus me-2"></i>New Template</button>
            </div>

            <div class="tab-menu">
                <div class="tab-item active">ALL</div>
                <div class="tab-item"><i class="fa-solid fa-pen" style="font-size:0.8rem;"></i></div>
            </div>

            <div class="table-custom">
                <table class="table mb-0">
                    <thead>
                        <tr>
                            <th style="width: 250px;">NAME</th>
                            <th style="width: 90px;">VERSION</th>
                            <th style="width: 120px;">STATUS</th>
                            <th style="width: 160px;">LAST TASK</th>
                            <th style="width: 180px;">PLAYBOOK</th>
                            <th style="width: 220px;">INVENTORY</th>
                            <th>VARIABLES</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <div class="d-flex align-items-center gap-2">
                                    <button class="btn-run" title="Run Playbook" onclick="runTask('Configure SAP', 'configure_SAP.yml', 'Walids machine for Sacrifice')"><i class="fa-solid fa-play" style="font-size:0.75rem;"></i></button>
                                    <span class="playbook-link" onclick="viewPlaybook('configure_SAP.yml')">Configure SAP</span>
                                </div>
                            </td>
                            <td>—</td>
                            <td><span class="badge-success-custom"><i class="fa-solid fa-circle-check"></i> Success</span></td>
                            <td><a href="#" onclick="viewTaskLog('#331', 'Tayeb ZEROUKI', 'Configure SAP')">#331</a><br><small class="text-muted">by Tayeb ZEROUKI</small></td>
                            <td><code>configure_SAP.yml</code></td>
                            <td>Walid's machine for Sacrifice</td>
                            <td class="text-muted">Empty</td>
                        </tr>

                        <tr>
                            <td>
                                <div class="d-flex align-items-center gap-2">
                                    <button class="btn-run" title="Run Playbook" onclick="runTask('Get RAM & CPU', 'get_ram_cpu.yml', 'Kawthar ADDA BENDIA')"><i class="fa-solid fa-play" style="font-size:0.75rem;"></i></button>
                                    <span class="playbook-link" onclick="viewPlaybook('get_ram_cpu.yml')">Get RAM & CPU</span>
                                </div>
                            </td>
                            <td>—</td>
                            <td><span class="badge-success-custom"><i class="fa-solid fa-circle-check"></i> Success</span></td>
                            <td><a href="#" onclick="viewTaskLog('#336', 'Tayeb ZEROUKI', 'Get RAM & CPU')">#336</a><br><small class="text-muted">by Tayeb ZEROUKI</small></td>
                            <td><code>get_ram_cpu.yml</code></td>
                            <td>Kawthar ADDA BENDIA</td>
                            <td class="text-muted">Empty</td>
                        </tr>

                        <tr>
                            <td>
                                <div class="d-flex align-items-center gap-2">
                                    <button class="btn-run" title="Run Playbook" onclick="runTask('Get Session', 'get_Session.yml', 'Karim ZEMRI')"><i class="fa-solid fa-play" style="font-size:0.75rem;"></i></button>
                                    <span class="playbook-link" onclick="viewPlaybook('get_Session.yml')">Get Session</span>
                                </div>
                            </td>
                            <td>—</td>
                            <td><span class="badge-success-custom"><i class="fa-solid fa-circle-check"></i> Success</span></td>
                            <td><a href="#" onclick="viewTaskLog('#337', 'Tayeb ZEROUKI', 'Get Session')">#337</a><br><small class="text-muted">by Tayeb ZEROUKI</small></td>
                            <td><code>get_Session.yml</code></td>
                            <td>Karim ZEMRI</td>
                            <td class="text-muted">Empty</td>
                        </tr>

                        <tr>
                            <td>
                                <div class="d-flex align-items-center gap-2">
                                    <button class="btn-run" title="Run Playbook" onclick="runTask('Install Chocolatey', 'install_chocolatey.yml', 'Walids machine for Sacrifice')"><i class="fa-solid fa-play" style="font-size:0.75rem;"></i></button>
                                    <span class="playbook-link" onclick="viewPlaybook('install_chocolatey.yml')">Install Chocolatey</span>
                                </div>
                            </td>
                            <td>—</td>
                            <td><span class="badge-success-custom"><i class="fa-solid fa-circle-check"></i> Success</span></td>
                            <td><a href="#" onclick="viewTaskLog('#34', 'administrateur', 'Install Chocolatey')">#34</a><br><small class="text-muted">by administrateur</small></td>
                            <td><code>install_chocolatey.yml</code></td>
                            <td>Walid's machine for Sacrifice</td>
                            <td class="text-muted">Empty</td>
                        </tr>

                        <tr>
                            <td>
                                <div class="d-flex align-items-center gap-2">
                                    <button class="btn-run" title="Run Playbook" onclick="runTask('Install Sap', 'install_sap.yml', 'Walids machine for Sacrifice')"><i class="fa-solid fa-play" style="font-size:0.75rem;"></i></button>
                                    <span class="playbook-link" onclick="viewPlaybook('install_sap.yml')">Install Sap</span>
                                </div>
                            </td>
                            <td>—</td>
                            <td><span class="badge-success-custom"><i class="fa-solid fa-circle-check"></i> Success</span></td>
                            <td><a href="#" onclick="viewTaskLog('#147', 'Walid DJELLALI', 'Install Sap')">#147</a><br><small class="text-muted">by Walid DJELLALI</small></td>
                            <td><code>install_sap.yml</code></td>
                            <td>Walid's machine for Sacrifice</td>
                            <td class="text-muted">Empty</td>
                        </tr>

                        <tr>
                            <td>
                                <div class="d-flex align-items-center gap-2">
                                    <button class="btn-run" title="Run Playbook" onclick="runTask('Install VNC', 'install-software.yml', 'AHMED BEAIBech')"><i class="fa-solid fa-play" style="font-size:0.75rem;"></i></button>
                                    <span class="playbook-link" onclick="viewPlaybook('install-software.yml')">Install VNC</span>
                                </div>
                            </td>
                            <td>—</td>
                            <td><span class="badge-success-custom"><i class="fa-solid fa-circle-check"></i> Success</span></td>
                            <td><a href="#" onclick="viewTaskLog('#184', 'Tayeb ZEROUKI', 'Install VNC')">#184</a><br><small class="text-muted">by Tayeb ZEROUKI</small></td>
                            <td><code>install-software.yml</code></td>
                            <td>AHMED BEAIBech</td>
                            <td class="text-muted">Empty</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Section: Inventory -->
        <div id="section-inventory" style="display: none;">
            <h1 class="page-title">Inventory</h1>
            <div class="table-custom">
                <table class="table mb-0">
                    <thead>
                        <tr>
                            <th>NAME</th>
                            <th>TYPE</th>
                            <th>USER</th>
                            <th>HOSTS FILE</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Walid's machine for Sacrifice</td><td><span class="badge bg-secondary">Static</span></td><td>ansibe</td><td><code>playbook/hosts</code></td></tr>
                        <tr><td>Kawthar ADDA BENDIA</td><td><span class="badge bg-secondary">Static</span></td><td>ansibe</td><td><code>playbook/hosts</code></td></tr>
                        <tr><td>Karim ZEMRI</td><td><span class="badge bg-secondary">Static</span></td><td>ansibe</td><td><code>playbook/hosts</code></td></tr>
                        <tr><td>AHMED BEAIBech</td><td><span class="badge bg-secondary">Static</span></td><td>ansibe</td><td><code>playbook/hosts</code></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Section: Generic -->
        <div id="section-generic" style="display: none;">
            <h1 class="page-title" id="generic-title">Section</h1>
            <div class="alert alert-info">Cette section est active en mode simulation locale pour le projet <strong>Remote Installation Manager</strong>.</div>
        </div>
    </div>
</div>

<!-- Modal Playbook Code -->
<div class="modal fade" id="modalPlaybook" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="modal-filename">Playbook Code</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <pre id="modal-code-content" class="modal-code"></pre>
            </div>
        </div>
    </div>
</div>

<!-- Modal Task Execution Log -->
<div class="modal fade" id="modalLog" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content bg-dark text-light">
            <div class="modal-header border-secondary">
                <h5 class="modal-title" id="modal-log-title">Task Log</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <pre id="modal-log-content" class="text-success" style="font-family: monospace; white-space: pre-wrap;"></pre>
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
    function showSection(section, element) {
        document.querySelectorAll('.nav-link-custom').forEach(el => el.classList.remove('active'));
        if(element) element.classList.add('active');

        document.getElementById('section-templates').style.display = 'none';
        document.getElementById('section-inventory').style.display = 'none';
        document.getElementById('section-generic').style.display = 'none';

        if(section === 'templates') {
            document.getElementById('section-templates').style.display = 'block';
        } else if(section === 'inventory') {
            document.getElementById('section-inventory').style.display = 'block';
        } else {
            document.getElementById('section-generic').style.display = 'block';
            document.getElementById('generic-title').innerText = element.innerText.trim();
        }
    }

    async function viewPlaybook(playbookFile) {
        document.getElementById('modal-filename').innerText = playbookFile;
        document.getElementById('modal-code-content').innerText = "Chargement du fichier...";
        const modal = new bootstrap.Modal(document.getElementById('modalPlaybook'));
        modal.show();

        const res = await fetch('/api/read?file=playbook/' + encodeURIComponent(playbookFile));
        const data = await res.json();
        document.getElementById('modal-code-content').innerText = data.content;
    }

    async function runTask(taskName, playbookFile, inventory) {
        document.getElementById('modal-log-title').innerText = "Execution Task: " + taskName;
        document.getElementById('modal-log-content').innerText = "Starting task #" + Math.floor(Math.random()*100 + 340) + " for " + taskName + "...\nRunning playbook " + playbookFile + " on inventory [" + inventory + "]...\n";
        const modal = new bootstrap.Modal(document.getElementById('modalLog'));
        modal.show();

        const res = await fetch('/api/test?file=playbook/' + encodeURIComponent(playbookFile));
        const data = await res.json();
        
        setTimeout(() => {
            document.getElementById('modal-log-content').innerText += "\n" + data.message + "\n\nTask Status: SUCCESS ✔";
        }, 800);
    }

    function viewTaskLog(taskId, user, taskName) {
        document.getElementById('modal-log-title').innerText = "Task " + taskId + " Log (" + taskName + ")";
        document.getElementById('modal-log-content').innerText = "Task " + taskId + " launched by " + user + "\nResult: SUCCESS ✔\nHost: 192.168.10.184\nPlaybook executed cleanly without errors.";
        const modal = new bootstrap.Modal(document.getElementById('modalLog'));
        modal.show();
    }
</script>
</body>
</html>
"""

class LocalHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/" or path == "/index.html" or path.startswith("/project"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode('utf-8'))
            return

        if path == "/api/read":
            fname = query.get('file', [''])[0]
            fpath = os.path.normpath(os.path.join(BASE_DIR, fname))
            if not fpath.startswith(BASE_DIR) or not os.path.exists(fpath):
                self.send_response(404)
                self.end_headers()
                return

            with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"content": content}).encode('utf-8'))
            return

        if path == "/api/test":
            fname = query.get('file', [''])[0]
            fpath = os.path.normpath(os.path.join(BASE_DIR, fname))
            
            msg = f"=== SEMAPHORE EXECUTION SIMULATION: {fname} ===\n"
            try:
                with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
                    lines = f.readlines()
                
                msg += f"PLAY [Target Remote Machine]\n"
                msg += "TASK [Gathering Facts] : ok\n"
                msg += f"TASK [Execute {fname}] : ok (Dry Run Completed)\n"
                msg += "PLAY RECAP : ok=2 changed=0 unreachable=0 failed=0\n"
                res = {"status": "ok", "message": msg}
            except Exception as e:
                res = {"status": "error", "message": f"Execution failed: {e}"}

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode('utf-8'))
            return

        super().do_GET()

socketserver.TCPServer.allow_reuse_address = True
print(f"Semaphore UI Local Replica starting on http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), LocalHandler) as httpd:
    httpd.serve_forever()
