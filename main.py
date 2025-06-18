from flask import Flask, request
import requests
import json

app = Flask(__name__)

TELEGRAM_TOKEN = "8117149892:AAGVS_me2cwH7qCmsYPBqWx-81MVZgUIXsY"
CHAT_ID = "698603211"

@app.route('/', methods=['POST'])
def webhook():
    try:
        data = json.loads(request.data.decode('utf-8'))

        direction = data.get("direction", "").upper()
        target = data.get("target")
        price = data.get("price")
        t1 = data.get("t1")
        t2 = data.get("t2")
        t3 = data.get("t3")

        if direction in ["CALL", "PUT"] and t1 and t2 and t3:
            arrow = "📈" if direction == "CALL" else "📉"
            msg = f"""{arrow} {direction} Signal Fired!
🎯 Target 1: ${t1}
🎯 Target 2: ${t2}
🎯 Target 3: ${t3}"""

        elif direction in ["CALL", "PUT"] and target and price:
            arrow = "📈" if direction == "CALL" else "📉"
            msg = f"✅ {direction} Target {target} reached at ${price}"

        elif direction == "FAIL":
            msg = "❌ Trade failed to hit any target"

        else:
            msg = f"📢 Trade update: {data}"

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
        return "ok"

    except Exception as e:
        return str(e), 400

