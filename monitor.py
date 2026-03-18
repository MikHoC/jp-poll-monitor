import requests
import json
import os

URL = "https://static-cdn.jyllands-posten.dk/editorial/data/polls-tracker/polls-data.json"
NTFY_TOPIC = os.environ["NTFY_TOPIC"]
TIMESTAMP_FILE = "last_timestamp.txt"

def get_timestamp():
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    return response.json()["metadata"]["update_timestamp"]

def send_notification(old_ts, new_ts):
    requests.post(
        f"https://ntfy.sh/{NTFY_TOPIC}",
        headers={
            "Title": "JP Meningsmålinger Opdateret! 📊",
            "Priority": "default",
            "Tags": "bar_chart"
        },
        data=f"Opdateret fra {old_ts} til {new_ts}"
    )
    print(f"✅ Notification sent! {old_ts} -> {new_ts}")

def monitor():
    current_timestamp = get_timestamp()
    print(f"Current timestamp: {current_timestamp}")

    # Read last known timestamp
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, "r") as f:
            last_timestamp = f.read().strip()
    else:
        last_timestamp = None
        print("No previous timestamp found - first run!")

    # Compare and notify
    if last_timestamp is None:
        print(f"First run - saving timestamp: {current_timestamp}")
    elif current_timestamp != last_timestamp:
        print(f"🔔 Update detected!")
        send_notification(last_timestamp, current_timestamp)
    else:
        print(f"No changes detected.")

    # Save current timestamp
    with open(TIMESTAMP_FILE, "w") as f:
        f.write(current_timestamp)

if __name__ == "__main__":
    monitor()
