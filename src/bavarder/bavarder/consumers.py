from channels import Group
import json


def ws_connect(message):
    """On Socket connection establishment"""
    print('Client connected')
    Group('chat').add(message.reply_channel)
    message.reply_channel.send({"accept": True})


def ws_receive(message):
    """On Socket receiving message"""
    print('Received message')
    message_obj = None
    try:
        message_obj = json.loads(message.content['text'])
        Group('chat').send({'text': json.dumps(message_obj)})
    except:
        print('Unable to parse json.')


def ws_disconnect(message):
    """On Socket connection disconnect"""
    print('Disconnected Socket')
    message.reply_channel.send({"accept": False})
    Group('chat').discard(message.reply_channel)
