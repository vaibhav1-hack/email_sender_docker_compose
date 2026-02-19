from flask import Flask, request, jsonify, render_template_string
from send_mail_update2 import send_bulk_emails
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

HTML = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SMTP Bulk Sender</title>
  <style>
    :root{
      --bg:#0b1020;
      --card:#111a33;
      --muted:#8ea0c9;
      --text:#eaf0ff;
      --line:rgba(255,255,255,.10);
      --accent:#6ea8fe;
      --accent2:#7ee787;
      --danger:#ff6b6b;
      --shadow: 0 20px 60px rgba(0,0,0,.35);
      --radius: 18px;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji","Segoe UI Emoji";
      background: radial-gradient(1200px 800px at 10% 10%, rgba(110,168,254,.20), transparent 60%),
                  radial-gradient(1200px 800px at 90% 20%, rgba(126,231,135,.12), transparent 55%),
                  var(--bg);
      color:var(--text);
    }
    .wrap{min-height:100vh; display:grid; place-items:center; padding:28px;}
    .shell{width:min(980px, 100%); display:grid; gap:16px;}
    .topbar{
      display:flex; align-items:center; justify-content:space-between;
      padding:18px 20px; border:1px solid var(--line); border-radius:var(--radius);
      background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
      box-shadow: var(--shadow);
    }
    .brand{display:flex; gap:12px; align-items:center}
    .logo{
      width:42px;height:42px;border-radius:14px;
      background: linear-gradient(135deg, rgba(110,168,254,.9), rgba(126,231,135,.85));
      box-shadow: 0 12px 28px rgba(110,168,254,.25);
    }
    .title{line-height:1.1}
    .title h1{margin:0; font-size:18px; font-weight:800; letter-spacing:.3px}
    .title p{margin:4px 0 0; font-size:13px; color:var(--muted)}
    .chip{
      font-size:12px; color:var(--muted);
      border:1px solid var(--line); padding:8px 10px; border-radius:999px;
      background: rgba(255,255,255,.03);
    }

    .grid{
      display:grid;
      grid-template-columns: 1.05fr .95fr;
      gap:16px;
    }
    @media (max-width: 900px){ .grid{grid-template-columns:1fr} }

    .card{
      border:1px solid var(--line);
      border-radius:var(--radius);
      background: rgba(255,255,255,.04);
      box-shadow: var(--shadow);
      padding:18px;
    }
    .card h2{margin:0 0 6px; font-size:16px}
    .card .sub{margin:0 0 14px; color:var(--muted); font-size:13px}

    label{display:block; margin-top:12px; font-size:12px; color:var(--muted)}
    input, textarea{
      width:100%;
      margin-top:6px;
      padding:12px 12px;
      border:1px solid var(--line);
      border-radius:14px;
      background: rgba(0,0,0,.18);
      color:var(--text);
      outline:none;
    }
    textarea{min-height:220px; resize:vertical}
    input:focus, textarea:focus{border-color: rgba(110,168,254,.55); box-shadow:0 0 0 3px rgba(110,168,254,.15)}

    .row{display:grid; grid-template-columns:1fr 1fr; gap:10px}
    @media (max-width: 520px){ .row{grid-template-columns:1fr} }

    .actions{display:flex; gap:10px; margin-top:14px; flex-wrap:wrap}
    button{
      border:0; border-radius:14px; cursor:pointer;
      padding:12px 14px; font-weight:700;
      color:var(--text);
      background: rgba(255,255,255,.06);
      border:1px solid var(--line);
    }
    .primary{
      background: linear-gradient(135deg, rgba(110,168,254,.95), rgba(110,168,254,.65));
      border-color: rgba(110,168,254,.35);
    }
    .ghost{background: transparent}
    button:disabled{opacity:.55; cursor:not-allowed}

    .toast{
      margin-top:12px;
      border-radius:14px;
      padding:12px 12px;
      border:1px solid var(--line);
      background: rgba(0,0,0,.18);
      color:var(--text);
      display:none;
      font-family: var(--mono);
      font-size:12px;
      white-space: pre-wrap;
    }
    .toast.ok{border-color: rgba(126,231,135,.35)}
    .toast.err{border-color: rgba(255,107,107,.45)}

    .hint{
      margin-top:10px;
      font-size:12px;
      color:var(--muted);
    }
    .kpi{
      display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:12px;
    }
    .kpi .box{
      border:1px solid var(--line);
      border-radius:16px;
      padding:12px;
      background: rgba(255,255,255,.03);
    }
    .kpi .num{font-size:20px; font-weight:900}
    .kpi .lab{font-size:12px; color:var(--muted)}
    pre{
      margin:12px 0 0;
      padding:12px;
      border-radius:16px;
      border:1px solid var(--line);
      background: rgba(0,0,0,.24);
      overflow:auto;
      font-family: var(--mono);
      font-size:12px;
      color:#d7e3ff;
      display:none;
      max-height: 320px;
    }
    .footer{
      text-align:center;
      color: rgba(234,240,255,.55);
      font-size:12px;
      margin-top:8px;
    }

    /* Login modal-ish panel */
    .loginWrap{
      display:none;
      grid-template-columns: 1fr;
    }
    .loginCard{
      max-width:520px;
      margin: 0 auto;
    }
    .pill{
      display:inline-flex; gap:8px; align-items:center;
      padding:8px 10px; border-radius:999px;
      border:1px solid var(--line);
      background: rgba(255,255,255,.03);
      color:var(--muted);
      font-size:12px;
    }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="shell">
      <div class="topbar">
        <div class="brand">
          <div class="logo"></div>
          <div class="title">
            <h1>SMTP Bulk Sender</h1>
            <p>Send a fixed message with throttling (10s) • Built for controlled internal use</p>
          </div>
        </div>
        <div class="chip" id="authChip">Not logged in</div>
      </div>

      <!-- LOGIN -->
      <div class="loginWrap" id="loginWrap" style="display:grid;">
        <div class="card loginCard">
          <h2>Admin Login</h2>
          <p class="sub">This UI gate is basic. Real protection should still be server-side.</p>

          <label>Username</label>
          <input id="u" placeholder="admin" autocomplete="username" />

          <label>Password</label>
          <input id="p" type="password" placeholder="admin123" autocomplete="current-password" />

          <div class="actions">
            <button class="primary" onclick="login()">Login</button>
            <button class="ghost" onclick="fillDemo()">Fill demo</button>
          </div>

          <div class="toast err" id="loginToast"></div>
          <div class="hint">
            Default creds (as requested): <span class="pill">admin / admin123</span>
          </div>
        </div>
      </div>

      <!-- APP -->
      <div class="grid" id="appWrap" style="display:none;">
        <div class="card">
          <h2>Recipients</h2>
          <p class="sub">Paste emails (newline or comma separated). Invalid entries get ignored.</p>

          <label>Emails</label>
          <textarea id="emails" placeholder="a@example.com&#10;b@example.com"></textarea>

          <div class="row">
            <div>
              <label>Delay (seconds)</label>
              <input id="delay" type="number" min="1" value="10" />
            </div>
            <div>
              <label>Max emails (safety)</label>
              <input id="max" type="number" min="1" value="150" />
            </div>
          </div>

          <div class="actions">
            <button class="primary" id="sendBtn" onclick="startSend()">Start sending</button>
            <button onclick="clearAll()">Clear</button>
            <button class="ghost" onclick="logout()">Logout</button>
          </div>

          <div class="toast" id="status"></div>
          <pre id="out"></pre>
        </div>

        <div class="card">
          <h2>Payload Preview</h2>
          <p class="sub">This is what will be sent to your backend endpoint <span class="pill">POST /send</span></p>

          <div class="kpi">
            <div class="box">
              <div class="num" id="count">0</div>
              <div class="lab">Valid recipients</div>
            </div>
            <div class="box">
              <div class="num" id="eta">0s</div>
              <div class="lab">Estimated delay time</div>
            </div>
          </div>

          <label>Fixed message</label>
          <input value="hi this is vaibhav" disabled />

          <label>JSON preview</label>
          <pre id="preview" style="display:block;"></pre>

          <div class="hint">
            If you expose this app publicly, you’re basically inviting abuse. Keep it behind auth + IP restriction.
          </div>
        </div>
      </div>

      <div class="footer">Tip: Use server-side auth + firewall rules. This UI login is just a convenience layer.</div>
    </div>
  </div>

<script>
  // UI-only login (NOT real security)
  const AUTH_KEY = "smtp_ui_authed";
  const DEFAULT_USER = "admin";
  const DEFAULT_PASS = "admin123";

  function isAuthed(){
    return sessionStorage.getItem(AUTH_KEY) === "1";
  }

  function showApp(){
    document.getElementById("loginWrap").style.display = "none";
    document.getElementById("appWrap").style.display = "grid";
    document.getElementById("authChip").textContent = "Logged in";
    refreshPreview();
  }

  function showLogin(){
    document.getElementById("appWrap").style.display = "none";
    document.getElementById("loginWrap").style.display = "grid";
    document.getElementById("authChip").textContent = "Not logged in";
  }

  function toast(id, msg, kind){
    const el = document.getElementById(id);
    el.style.display = "block";
    el.className = "toast " + (kind || "");
    el.textContent = msg;
  }

  function fillDemo(){
    document.getElementById("u").value = DEFAULT_USER;
    document.getElementById("p").value = DEFAULT_PASS;
  }

  function login(){
    const u = (document.getElementById("u").value || "").trim();
    const p = (document.getElementById("p").value || "").trim();
    const t = document.getElementById("loginToast");
    t.style.display = "none";

    if (u === DEFAULT_USER && p === DEFAULT_PASS){
      sessionStorage.setItem(AUTH_KEY, "1");
      showApp();
    } else {
      toast("loginToast", "Invalid credentials.", "err");
    }
  }

  function logout(){
    sessionStorage.removeItem(AUTH_KEY);
    showLogin();
  }

  function splitEmails(raw){
    const parts = (raw || "").replace(/\n/g, ",").split(",");
    const out = [];
    for (const p of parts){
      const e = p.trim();
      if (!e) continue;
      // basic sanity check
      if (e.includes("@") && e.includes(".")) out.push(e);
    }
    // dedupe
    return [...new Set(out)];
  }

  function refreshPreview(){
    const emails = document.getElementById("emails").value;
    const delay = parseInt(document.getElementById("delay").value || "10", 10);
    const max = parseInt(document.getElementById("max").value || "150", 10);

    const list = splitEmails(emails).slice(0, max);
    document.getElementById("count").textContent = list.length;
    document.getElementById("eta").textContent = (Math.max(0, list.length - 1) * delay) + "s";

    const payload = { emails: list.join("\n"), delay_seconds: delay, max_emails: max };
    document.getElementById("preview").textContent = JSON.stringify(payload, null, 2);
  }

  function clearAll(){
    document.getElementById("emails").value = "";
    toast("status", "Cleared.", "");
    document.getElementById("out").style.display = "none";
    refreshPreview();
  }

  async function startSend(){
    if (!isAuthed()){
      showLogin();
      return;
    }

    const raw = document.getElementById("emails").value;
    const delay = parseInt(document.getElementById("delay").value || "10", 10);
    const max = parseInt(document.getElementById("max").value || "150", 10);

    const list = splitEmails(raw);
    if (list.length === 0){
      toast("status", "Paste at least one valid email.", "err");
      return;
    }
    if (list.length > max){
      toast("status", `Too many emails. Max allowed is ${max}.`, "err");
      return;
    }

    const btn = document.getElementById("sendBtn");
    btn.disabled = true;
    toast("status", "Sending... do not close this tab.", "");

    try{
      // backend expects {emails: raw_string}
      // we also send delay/max for UI display; backend can ignore or use it if you implement.
      const res = await fetch("/send", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ emails: list.join("\n"), delay_seconds: delay, max_emails: max })
      });

      const data = await res.json();
      if (!data.ok){
        throw new Error(data.error || "Unknown error");
      }

      toast("status", `Done. Sent: ${data.sent?.length || 0}, Failed: ${data.failed?.length || 0}`, "ok");
      const out = document.getElementById("out");
      out.style.display = "block";
      out.textContent = JSON.stringify(data, null, 2);
    }catch(e){
      toast("status", "Failed: " + e.message, "err");
    }finally{
      btn.disabled = false;
    }
  }

  // listeners
  document.addEventListener("input", (e) => {
    if (["emails","delay","max"].includes(e.target.id)) refreshPreview();
  });

  // init
  if (isAuthed()) showApp(); else showLogin();
</script>
</body>
</html>
"""


@app.get("/")
def home():
    return render_template_string(HTML)

@app.post("/send")
def send():
    data = request.get_json(force=True) or {}
    raw = (data.get("emails") or "").strip()

    # split by newline and commas
    parts = raw.replace("\n", ",").split(",")
    recipients = [p.strip() for p in parts if p.strip()]

    try:
        results = send_bulk_emails(recipients, delay_seconds=10)
        return jsonify({"ok": True, **results})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

