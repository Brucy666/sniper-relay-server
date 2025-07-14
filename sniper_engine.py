import os
import time
import requests

# Basic config
KUCOIN_SYMBOL = "BTC-USDT"
DISCORD_WEBHOOK = os.getenv("WEBHOOK_URL")

# Simulated logic — to be replaced by real data feeds
def get_mock_data():
    return {
        "symbol": KUCOIN_SYMBOL,
        "price": 58234.50,
        "vwap": 58100.00,
        "spoof_ratio": 0.68,
        "bias": "Below",
        "trap_type": "VWAP Rejection",
        "rsi_status": "RSI V-Split Confirmed",
        "confidence": 9,
        "score": 92,
    }

# Format Discord alert
def format_discord_alert(trade_data):
    emoji = "📉" if trade_data["bias"] == "Below" else "📈"
    spoof_emoji = "🟡" if trade_data["spoof_ratio"] < 0.3 else "🟠" if trade_data["spoof_ratio"] < 0.6 else "🔴"
    confidence_emoji = "🧠" if trade_data["confidence"] >= 8 else "⚠️" if trade_data["confidence"] >= 5 else "❓"
    rsi_emoji = "💥" if "split" in trade_data["rsi_status"].lower() else "🌀"

    return {
        "username": "QuickStrike Bot",
        "embeds": [{
            "title": "🎯 BTC Sniper Alert",
            "color": 0xff5555 if trade_data["bias"] == "Below" else 0x00ffae,
            "fields": [
                {"name": "Token", "value": f"`{trade_data['symbol']}`", "inline": True},
                {"name": "Bias", "value": f"{emoji} `{trade_data['bias']}`", "inline": True},
                {"name": "Spoof Ratio", "value": f"{spoof_emoji} `{trade_data['spoof_ratio']:.3f}`", "inline": True},
                {"name": "Trap Type", "value": f"`{trade_data['trap_type']}`", "inline": True},
                {"name": "RSI", "value": f"{rsi_emoji} `{trade_data['rsi_status']}`", "inline": True},
                {"name": "Confidence", "value": f"{confidence_emoji} `{trade_data['confidence']}/10`", "inline": True},
                {"name": "Score", "value": f"`{trade_data['score']}`", "inline": True},
            ],
            "footer": {"text": "QuickStrike Engine v1"}
        }]
    }

# Send alert
def send_discord_alert(data):
    if DISCORD_WEBHOOK:
        alert = format_discord_alert(data)
        try:
            res = requests.post(DISCORD_WEBHOOK, json=alert)
            print("[+] Alert sent:", res.status_code)
        except Exception as e:
            print("[!] Failed to send alert:", e)
    else:
        print("[!] DISCORD_WEBHOOK not set.")

# Main loop
if __name__ == "__main__":
    print("[*] Starting sniper engine for BTC...")
    while True:
        trade_data = get_mock_data()
        print("[~] Scanned:", trade_data)
        if trade_data["confidence"] >= 8 and trade_data["score"] >= 90:
            send_discord_alert(trade_data)
        time.sleep(60)  # scan every 60s
