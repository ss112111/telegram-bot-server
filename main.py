from flask import Flask, request
import requests
import json

app = Flask(__name__)

TELEGRAM_TOKEN = "8117149892:AAGVS_me2cwH7qCmsYPBqWx-81MVZgUIXsY"
CHAT_ID = "698603211"
CHANNEL_ID = "-1002884178515"  # <-- your channel

...

# Send to personal
url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# Send to channel
requests.post(url, data={"chat_id": CHANNEL_ID, "text": msg})


@app.route('/', methods=['POST'])
def webhook():
    try:
        # Log the raw body
        raw_body = request.data.decode('utf-8')
        print(f"🔹 Raw webhook received: {raw_body}")

        # Try parsing JSON
        data = json.loads(raw_body)

        direction = data.get("direction", "").upper()
        target = data.get("target")
        price = data.get("price")
        t1 = data.get("t1")
        t2 = data.get("t2")
        t3 = data.get("t3")

        # Message format: full signal with 3 targets
        if direction in ["CALL", "PUT"] and t1 is not None and t2 is not None and t3 is not None:

            arrow = "📈" if direction == "CALL" else "📉"
            msg = f"""{arrow} {direction} Signal Fired!
🎯 Target 1: ${t1}
🎯 Target 2: ${t2}
🎯 Target 3: ${t3}"""

        # Message format: target reached
        elif direction in ["CALL", "PUT"] and target and price:
            arrow = "📈" if direction == "CALL" else "📉"
            msg = f"✅ {direction} Target {target} reached at ${price}"

        # Fail message
        elif direction == "FAIL":
            msg = "❌ Trade failed to hit any target"

        # Fallback for malformed structure
       else:
    msg = f"⚠️ Unrecognized format:\n{json.dumps(data)}"

        # Send to Telegram
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

        return "ok"

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return "Invalid JSON", 400

