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

        direction = data.get("direction", "").upper()  # CALL or PUT or FAIL
        price = data.get("price")  # predicted price level (optional)

        if direction in ["CALL", "PUT"] and price:
            arrow = "📈" if direction == "CALL" else "📉"
            msg = f"{arrow} {direction} Target → Predicted price: ${price}"
        elif direction == "FAIL":
            msg = "❌ Trade failed to hit any target"
        else:
            msg = f"📢 Trade update: {data}"

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
        return "ok"

    except Exception as e:
        return str(e), 400
