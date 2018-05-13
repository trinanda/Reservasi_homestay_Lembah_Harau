# Yang ini sudah bisa, namun hanya baru ke number yang sudah di verified

from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACe211524106753eb639d9fae6ebd35bb2"
# Your Auth Token from twilio.com/console
auth_token  = "2d7c15d4df5846d341c3a67a7fec9b9b"

client = Client(account_sid, auth_token)

message = client.messages.create(
    # to="+6282174853636",/up
    to="+6281275803651",
    from_="+12014307127",
    body="Hello from Python-Twilo!")

print(message.sid)


