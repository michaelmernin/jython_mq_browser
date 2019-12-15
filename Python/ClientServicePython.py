from com.mqclient.mqbrowser import ClientService

import json
from dpath import dpath
import pymqi
import yaml
from pymqi import *

class ClientServicePython(ClientService):

    def __init__(self):

        conn_info = '%s(%s)' % (host, port)
        self.qmgr = pymqi.connect(queue_manager, channel, conn_info)
        self.get_queue = pymqi.Queue(self.qmgr, queue_name)
        gqdesc = od(ObjectName=queue_name)
        self.browse_q = Queue(self.qmgr, gqdesc, CMQC.MQOO_BROWSE)

    def get_messages(self):
        """Reads and returns all messages in the queue... Will delete messages from queue"""
        msg_list = list()
        self.get_queue.get()
        while True:
            message = self.get_queue.get().decode("utf-8")
            if not message:
                break
            msg_list.append(message)
        return msg_list

    def purge(self):
        """Purges queue"""
        count = 0
        try:
            while True:
                self.get_queue.get()
        except MQMIError:
            print("messages purged " + str(count))

    def close(self):
        self.get_queue.close()
        self.browse_q.close()
        self.qmgr.disconnect()

    def search_for_msgs(self, accounts):
        accounts = set(accounts)
        messages = []
        getOpts = gmo(Options=CMQC.MQGMO_BROWSE_NEXT)
        getOpts.WaitInterval = CMQC.MQWI_UNLIMITED
        msgDesc = md()
        count = 0
        while True:
            try:
                m = self.browse_q.get(None, msgDesc, getOpts).decode("utf-8")
            except MQMIError as e:
                print("queue emptied")
                print("messages counted " + str(count))
                break
            count = count + 1
            msg = json.loads(m)
            data = msg['data']
            # Retrieves message key dict
            msg_key_dict = dpath.get(data, "*Key")
            # Retrieves all key numbers from message key dict
            appl_nbr = set(dpath.values(msg_key_dict, "*Nbr*"))
            # checks if key matches a searching key
            if not appl_nbr.issubset(accounts):
                msgDesc['MsgId'] = bytes('', 'utf-8')
                msgDesc['CorrelId'] = bytes('', 'utf-8')
                continue

            # Retrieves key name message key dict
            msg_key = list(dpath.search(data, "*Key").keys())[0]
            messages.append(msg)
            time = msg.get('time', None)
            msg_name = data['msgDtl']['msgNme']
            app_cde = data[msg_key]['AppCde']

            msgDesc['MsgId'] = bytes('', 'utf-8')
            msgDesc['CorrelId'] = bytes('', 'utf-8')

        if len(messages) == 0:
            print("No messages found for ApplNbr " + str(accounts))

        return messages

    def browse_messages_return_all_as_string(self):
        messages = []
        getOpts = gmo(Options=CMQC.MQGMO_BROWSE_NEXT)
        getOpts.WaitInterval = CMQC.MQWI_UNLIMITED
        msgDesc = md()
        count = 0
        while True:
            try:
                m = self.browse_q.get(None, msgDesc, getOpts).decode("utf-8")
                messages.append(m)
                msgDesc['MsgId'] = bytes('', 'utf-8')
                msgDesc['CorrelId'] = bytes('', 'utf-8')
                count = count + 1
            except MQMIError:
                return messages





# def search_for_messages(self):
#         return "xxxx"