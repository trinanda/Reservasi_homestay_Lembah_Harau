import base64
import httplib2

from email.mime.text import MIMEText

from flask import Flask, request, render_template
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow


# Path to the client_secret.json file downloaded from the Developer Console
CLIENT_SECRET_FILE = 'client_secret.json'

# Check https://developers.google.com/gmail/api/auth/scopes for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.compose'

# Location of the credentials storage file
STORAGE = Storage('gmail.storage')

# Start the OAuth flow to retrieve credentials
flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
http = httplib2.Http()

# Try to retrieve credentials from storage or run the flow to generate them
credentials = STORAGE.get()
if credentials is None or credentials.invalid:
    credentials = run_flow(flow, STORAGE, http=http)

# Authorize the httplib2.Http object with our credentials
http = credentials.authorize(http)

# Build the Gmail service from discovery
gmail_service = build('gmail', 'v1', http=http)


app = Flask(__name__)


@app.route('/testinggmail', methods=['POST', 'GET'])
def email_pemesan():

    nama = 'Abdi'
    umur = '28'
    alamat = 'Surabaya'
    pekerjaan = 'pengusaha'

    pesannya = 'Nama dia' + nama + 'umurnya' + umur + 'dan' + nama + 'tinggal di' + alamat + 'sedangkan pekerjaannya adalah' + pekerjaan


    if request.method == 'POST':
        email_pemesan = request.form.get('EMAIL_PEMESAN')
        message_to_pemesan = MIMEText(pesannya)
        message_to_pemesan['to'] = email_pemesan
        message_to_pemesan['from'] = "zidanecr7kaka@gmail.com"
        message_to_pemesan['subject'] = "TESTING"
        raw_to_pemesan = base64.urlsafe_b64encode(message_to_pemesan.as_bytes())
        raw_to_pemesan = raw_to_pemesan.decode()
        body_to_pemesan = {'raw': raw_to_pemesan}

        # send it
        try:
          message_to_pemesan = (gmail_service.users().messages().send(userId="me", body=body_to_pemesan).execute())
          print('Message Id: %s' % message_to_pemesan['id'])
          print(message_to_pemesan)
        except Exception as error:
          print('An error occurred: %s' % error)

        return render_template('form.html')

    return render_template('form.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999, debug=True)
