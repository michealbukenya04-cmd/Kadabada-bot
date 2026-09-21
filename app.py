from flask import Flask, request, render_template_string
import requests, datetime, os
from collections import deque
app = Flask(__name__)
TOKEN = os.environ.get("TOKEN")
PHONE_ID = os.environ.get("PHONE_ID")
VERIFY_TOKEN = "kadabada123"
LOGS = deque(maxlen=50)
DASHBOARD_HTML = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{background:#0a0a0a;color:#fff;font-family:sans-serif;padding:15px;text-align:center}.card{background:#1a1a1a;padding:15px;border-radius:12px;margin:10px 0;border:1px solid #333}.green{color:#25D366}.log{font-size:12px;text-align:left;background:#000;padding:10px;border-radius:8px}</style></head><body><h2>🤖 KADABADA BOT <span class="green">● LIVE</span></h2><div class="card">Total: {{count}} | Time: {{time}}</div><div class="card"><h3>Live Logs</h3><div class="log">{{logs}}</div></div></body></html>"""
def send_reply(to, text):
    url = f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {"messaging_product":"whatsapp","to":to,"text":{"body":text}}
    requests.post(url, headers=headers, json=data)
@app.route('/')
def dashboard():
    logs_html = "<br>".join([f"{l['time']} - {l['from']}: {l['msg']}" for l in LOGS]) or "No messages yet. Send.ping to your bot!"
    return render_template_string(DASHBOARD_HTML, count=len(LOGS), time=datetime.datetime.now().strftime("%H:%M:%S"), logs=logs_html)
@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Fail",403
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    try:
        msg = data['entry'][0]['changes'][0]['value']['messages'][0]
        from_n = msg['from']; text = msg['text']['body']
        LOGS.append({"from":from_n,"msg":text,"time":datetime.datetime.now().strftime("%H:%M:%S")})
        if ".ping" in text.lower(): send_reply(from_n, "✅ ONLINE Chief! Dashboard is working!")
        elif ".riddle" in text.lower(): send_reply(from_n, "🧠 I brought sugar on your table with my physical energy. Who am I?")
        else: send_reply(from_n, f"Got: {text}. Try.ping or.riddle")
    except: pass
    return "OK",200
if __name__=="__main__": app.run(host="0.0.0.0", port=10000)
