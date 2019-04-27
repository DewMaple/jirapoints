#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

import schedule

from skype_api import skype_api
from jira_api import jira_api

def get_chat_for_urp_iteration(self):
        chat = None
        chats = None
        if self.skype.check_status() == 0:
            chats = self.skype.skype.Chats
        else:
            print("Cannot attach with skype!")

        for c in list(chats):
            if c.Topic == 'URP-Iteration':
                chat = c
                break


        if chat is None:
            chat = self.skype.CreateChatWith('admin')
            for f in list(self.skype.skype.Friends):
                if f.FullName in self.skype_list:
                    chat.AddMembers(f)
            chat._SetTopic('URP-Iteration')

        return chat

def recalculate_iteration(self):
        current_date = time.strptime("%w")
        if current_date != self.iteration_start_day:
            self.is_calculated = False
        else:
            self.current_iteration += 1
            self.is_calculated = True

def get_iter_result(self):
        jira = jira_api()
        issues = jira.get_issues('URP-BETA', self.current_iteration)

        head = 'iteration: ' + str(self.current_iteration) + '\n' + \
               'total stories(bugs): ' + str(issues.total) + '\n' + \
               'total points: ' + str(jira.count_story_points(issues)) + '\n'

        body = '------------------This is a line--------------------------' + '\n' + \
               str(jira.ready_to_dev_stories) + ' stories(bugs) is ready to dev, ' + str(jira.ready_to_dev_points) + \
               ' points' + '\n' + \
               str(jira.in_dev_stories) + ' stories(bugs) is in dev, ' + str(jira.in_dev_points) + ' points' + '\n\n'

        attention_in_test = '----In test----\n' + str(
            jira.ready_to_test_stories) + ' stories(bugs) is ready to test, ' + str(jira.ready_to_test_points) + \
                            ' points\n' + str(jira.in_test_stories) + ' stories(bugs) is in test, ' + str(
            jira.in_test_points) + ' points' + '\n\n'

        attention_done = '---Done---\n' + str(jira.ready_to_deliver_stories) + ' stories(bugs) is ready to deliver, ' + \
                         str(jira.ready_to_deliver_points) + ' points' + '\n' + \
                         str(jira.archived_stories) + ' stories(bugs) has been done, ' + \
                         str(jira.archived_points) + ' points \n'

        result = head + body + attention_in_test + attention_done
        print result
        return result

def daily_job(self, mess):
    chat = self.get_chat_for_urp_iteration()
    skype_api.send_massage_to_chat(chat, mess)

class jira_urp:
    def __init__(self):
        self.skype = skype_api.get_instance()
        self.current_iteration = 1
        self.iteration_duration = 7
        self.iteration_start_day = 5
        self.is_calculated = False
        self.skype_list = ('aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg', 'hhh')

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        if key == 'current_iteration':
            self.is_calculated = True

if __name__ == '__main__':
    iteration = 37
    j_urp = jira_urp()
    j_urp.current_iteration = 40
    schedule.every().day.at('9:40').do(j_urp.daily_job)
    mess = get_iter_result()
    # j_urp.daily_job(mess)

    while True:
        schedule.run_pending()
        inputs = raw_input()
        command = inputs.split(' ')
        if command[0] == 'audit':
            if len(command) > 1:
                j_urp.current_iteration = int(command[1])
                daily_job(mess)
            else:
                daily_job(mess)
        time.sleep(1)