from flask import Flask, request, jsonify
from flask_cors import CORS
from scheduler import parse_meeting_details
from email_utils import send_meeting_email

app = Flask(__name__)
CORS(app)

# -----------------------------
# IN-MEMORY STORE (TEMPORARY)
# -----------------------------
MEETINGS = []

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})

# -----------------------------
# SCHEDULE MEETING
# -----------------------------
@app.post("/api/schedule")
def schedule_meeting():
    data = request.get_json()
    query = data.get("query")
    emails = data.get("emails")

    if not query or not emails:
        return jsonify({"error": "Query and emails required"}), 400

    # Extract meeting details from AI/parser
    meeting = parse_meeting_details(query)

    # Process participant emails
    email_list = [e.strip() for e in emails.split(",") if e.strip()]
    email_results = []
    success_count = 0

    for email in email_list:
        success = send_meeting_email(email, meeting)
        email_results.append({"email": email, "status": "Sent" if success else "Failed"})
        if success:
            success_count += 1

    # Save meeting to in-memory store
    meeting_entry = meeting.copy()
    meeting_entry.update({
        "id": len(MEETINGS) + 1,
        "participants": email_list,
        "status": "confirmed"
    })
    MEETINGS.append(meeting_entry)

    # API response
    response = {
        "meeting": meeting_entry,
        "successful_emails": success_count,
        "total_emails": len(email_list),
        "email_results": email_results
    }

    return jsonify(response), 200

# -----------------------------
# GET ALL MEETINGS
# -----------------------------
@app.get("/api/meetings")
def get_meetings():
    return jsonify({"meetings": MEETINGS})

# -----------------------------
# EMAIL LOGS (TEMP)
# -----------------------------
@app.get("/api/email-logs")
def get_email_logs():
    # Placeholder until real logging added
    logs = []
    for meeting in MEETINGS:
        for email in meeting.get("participants", []):
            logs.append({"meeting_id": meeting["id"], "email": email, "status": "Sent"})
    return jsonify({"logs": logs})

# -----------------------------
# DASHBOARD STATS (TEMP)
# -----------------------------
@app.get("/api/stats")
def get_stats():
    total_meetings = len(MEETINGS)
    total_emails = sum(len(m.get("participants", [])) for m in MEETINGS)
    return jsonify({"totalMeetings": total_meetings, "emailsSent": total_emails})

# HOME ROUTE
@app.get("/")
def home():
    return "<h1>Backend is running. Use /api/... endpoints.</h1>"

# RUN APP
if __name__ == "__main__":
    app.run(debug=True)