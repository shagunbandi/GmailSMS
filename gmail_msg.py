import imaplib
import email
from twilio.rest import TwilioRestClient


def get_first_payload(body):
    try:
        return get_first_payload(body.get_payload()[0])
    except:
        return body.get_payload()


def read_mails(email_id, password):
    connection = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    connection.login(email_id, password)
    connection.select('INBOX', readonly=True)
    status, response = connection.uid('search', None, 'UNSEEN')
    if status == 'OK':
        unread_msg_nums = response[0].split()
    else:
        unread_msg_nums = []
    data_list = []
    for e_id in unread_msg_nums:
        data_dict = {}
        e_id = e_id.decode('utf-8')
        _, response = connection.uid('fetch', e_id, '(RFC822)')
        html = response[0][1].decode('utf-8')
        email_message = email.message_from_string(html)
        data_dict['mail_to'] = email_message['To']
        data_dict['mail_subject'] = email_message['Subject']
        data_dict['mail_from'] = email.utils.parseaddr(email_message['From'])
        data_dict['body'] = get_first_payload(email_message)
        data_list.append(data_dict)
    return data_list


def send_sms(msg_list, twilio_sid, twilio_token, twilio_to, twilio_from):
    client = TwilioRestClient(twilio_sid, twilio_token)
    for msg in msg_list:
        # body = 'from: '+str(msg['mail_from'])+'\nsubject: '+str(msg['mail_subject']) +'\nbody: '+str(msg['body'])
        body = 'from: '+str(msg['mail_from'])+'\nsubject: '+str(msg['mail_subject'])
        client.messages.create(
            to=twilio_to,
            from_=twilio_from,
            body=body
        )

email_id = 'someone@gmail.com'
password = 'XXXX'
twilio_sid = 'TWILIO_SID_HERE'
twilio_token = 'TWILIO_TOKEN_HERE'
twilio_to = '9898XXXX98'
twilio_from = '9898XXXX98'

msg_list = read_mails(email_id, password)
# for msg in msg_list:
#     body = 'from: ' + str(msg['mail_from']) + '\nsubject: ' + str(msg['mail_subject']) + '\nbody: ' + str(msg['body'])[:100]
#     print(body)
#     print('\n---\n')

send_sms(msg_list, twilio_sid, twilio_token, twilio_to, twilio_from)