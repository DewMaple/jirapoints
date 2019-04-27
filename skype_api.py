#!/usr/bin/python
# -*- coding: utf-8 -*-

import Skype4Py
from Skype4Py.chat import *


class skype_api:

    instance = None

    def __init__(self):
        self.skype = Skype4Py.Skype()
        self.current_user = self.skype.CurrentUser
        if self.skype.AttachmentStatus != 0:
            self.skype.Attach()

    def attach(self):
        if self.skype.AttachmentStatus != 0:
            self.skype.Attach()

    def get_chat_by_topic(self, topic):
        chat = None
        for c in list(self.skype.Chats):
            if c.Topic == topic:
                chat = c
                break

        if chat is None:
            chat = self.skype.CreateChatWith('me')
            for f in self.skype.SearchForUsers('another'):
                chat.AddMembers(f)
            chat._SetTopic(topic)

        return chat

    def check_status(self):
        if self.skype.AttachmentStatus != 0:
            self.skype.Attach()
        return self.skype.AttachmentStatus

    @staticmethod
    def send_massage_to_chat(chat, msg):
        for m in chat.Members:
            print m.FullName
        if isinstance(chat, Chat) and chat is not None:
            chat.SendMessage(msg)
        else:
            raise ValueError('ERROR!!! Wrong chat.')

    @staticmethod
    def get_instance():
        if skype_api.instance is not None:
            return skype_api.instance
        else:
            return skype_api()