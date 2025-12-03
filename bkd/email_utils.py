import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_meeting_email(to_email, meeting_details):
    sender_email = "shiwammaddheshiya@gmail.com"
    sender_password = "rtgi iasu sinu jiai"

    subject = f"Meeting Scheduled: {meeting_details['title']}"
    
    # Use HTML email so links are clickable
    platform_link = meeting_details.get('platform_link', '').strip()
    link_html = f'<br><a href="{platform_link}" target="_blank" style="color: #1a73e8;">Join Meeting Link</a>' if platform_link else ''
    
    body_html = f"""
    <html>
      <body>
        <p>Hello,</p>
        <p>Your meeting "<strong>{meeting_details['title']}</strong>" has been scheduled.</p>
        <p>
          <strong>Date:</strong> {meeting_details['date']}<br>
          <strong>Time:</strong> {meeting_details['time']}<br>
          <strong>Duration:</strong> {meeting_details['duration']}<br>
          <strong>Platform:</strong> {meeting_details['platform']} {link_html}
        </p>
        <p>Regards,<br>Intelligent Meeting Scheduler</p>
      </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    
    # Attach both plain and HTML versions (for fallback)
    plain_body = f"""
    Hello,

    Your meeting "{meeting_details['title']}" has been scheduled.

    Date: {meeting_details['date']}
    Time: {meeting_details['time']}
    Duration: {meeting_details['duration']}
    Platform: {meeting_details['platform']}
    {platform_link if platform_link else ''}

    Regards,
    Intelligent Meeting Scheduler
    """

    part1 = MIMEText(plain_body, "plain")
    part2 = MIMEText(body_html, "html")
    msg.attach(part1)
    msg.attach(part2)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"✅ Email sent successfully to {to_email}")
            return True
    except Exception as e:
        print(" Error sending email:", e)
        return False
