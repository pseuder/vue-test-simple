from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from oauth2client.file import Storage
from oauth2client import client, tools
from googleapiclient import discovery
import base64, os, httplib2

import variable

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'license server'

def get_credentials():
    credential_dir = os.path.join(os.getcwd(), '.credentials')
    CLIENT_SECRET_FILE = os.path.join(credential_dir, 'client_secret.json')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'gmail-api-send.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)

    return credentials

def CreateMessageHtml(to, cc, subject, msgHtml):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = variable.Sender_email_account
    msg['To'] = to
    msg['Cc'] = cc
    msg.attach(MIMEText(msgHtml.encode('utf-8'), 'html', 'utf-8'))
    #msg.attach(MIMEText(msgHtml, 'html'))
    return {'raw': (base64.urlsafe_b64encode(msg.as_bytes())).decode("utf-8") }


def SendMessageInternal(service, user_id, message):
    message = (service.users().messages().send(userId=user_id, body=message).execute())
    return message


def SendMessage(to, cc, subject, context, byte_msg=''):
    """
    to: <str>
    cc: 'address1;address2'
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    user_id = 'me'
    msgHtml = context

    if byte_msg != '':
        message = byte_msg
    else:
        message = CreateMessageHtml(to, cc, subject, msgHtml)
    result = SendMessageInternal(service, user_id, message)
    return result

# 手動更新憑證
if __name__ == '__main__':
    get_credentials()