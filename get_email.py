# pip install lxml
from oauth2client.file import Storage
from oauth2client import client, tools
import base64, os
import os.path

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify', 
          'https://www.googleapis.com/auth/gmail.labels']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'license server'

def get_credentials():
    credential_dir = os.path.join(os.getcwd(), '.credentials')
    CLIENT_SECRET_FILE = os.path.join(credential_dir, 'client_secret.json')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'gmail-api-read.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
    return credentials

def get_subject(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    payld = message['payload'] # get payload of the message 
    headr = payld['headers'] # get header of the payload
    for one in headr: # getting the Subject
        if one['name'] == 'Subject':
            return one['value']
        else:
            pass
    return 'None'

def get_sender(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    payld = message['payload'] # get payload of the message 
    headr = payld['headers'] # get header of the payload
    for three in headr: # getting the Sender
        if three['name'] == 'From':
            return three['value']
        else:
            pass
    return 'None'


def get_content(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    payld = message['payload'] # get payload of the message 
    # Fetching message body
    mssg_parts = payld['parts'] # fetching the message parts
    part_one  = mssg_parts[0] # fetching first element of the part 
    part_body = part_one['body'] # fetching body of the message
    part_data = part_body['data'] # fetching data from the body
    clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
    clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
    clean_two = base64.b64decode (clean_one) # decoding from Base64 to UTF-8
    clean_two = clean_two.decode("UTF-8")
    return clean_two
    

def get_label(service, user_id, msg_id, labels_map):
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()
    labelIds = message['labelIds'] # get labelIds of the message 
    # convert label ids to names
    for lab_index in range(len(labelIds)):
        labelIds[lab_index] = labels_map.get(labelIds[lab_index])
    return labelIds


def add_label(service, user_id, msg_id, labels_map, label_name):
    label_id = ''
    for lab in labels_map.keys():
        if(label_name == labels_map[lab]):
            label_id = lab
    label_body = {'addLabelIds':label_id}
    service.users().messages().modify(userId=user_id, id=msg_id, body=label_body).execute()

# 手動更新憑證
if __name__ == '__main__':
    get_credentials()