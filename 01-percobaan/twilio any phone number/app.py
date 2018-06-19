# Yang ini sudah bisa, namun hanya baru ke number yang sudah di verified

from twilio.rest import Client

# Your Account SID from twilio.com/console

# sid upgraded
account_sid = "ACe211524106753eb639d9fae6ebd35bb2"

#sid non upgrade
# account_sid = "ACe335c5f83a4c6a3dc22f25cb5fe3d74d"

# auth upgraded
# Your Auth Token from twilio.com/console
auth_token  = "2d7c15d4df5846d341c3a67a7fec9b9b"

# auth non upgradez
# auth_token  = "98f8f99a6bcbe14e0f5b9ab50ae55a31"

client = Client(account_sid, auth_token)

pesan_user = 'hello testing test'

message = client.messages.create(
    # to="+6281275803651",
    to="+6282283228532",    #agi

    # upgraded number
    from_="+12014307127",

    # non upgrade
    # from_="+12132961837",

    # from_="HRRS",
    body=pesan_user)

print(message.sid)

# 19.8848


