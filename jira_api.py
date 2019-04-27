#!/usr/bin/python
# -*- coding: utf-8 -*-

from jira.client import JIRA


class jira_api:
    def __init__(self):
        options = {
            'server': 'https://jira-server.com',
        }

        self.jira = JIRA(basic_auth=('admin', 'admin'), options=options)

        self.total_stories = 0
        self.total_points = 0

        self.ready_to_dev_points = 0
        self.ready_to_dev_stories = 0

        self.in_dev_points = 0
        self.in_dev_stories = 0

        self.ready_to_test_points = 0
        self.ready_to_test_stories = 0

        self.in_test_points = 0
        self.in_test_stories = 0

        self.ready_to_deliver_points = 0
        self.ready_to_deliver_stories = 0

        self.archived_points = 0
        self.archived_stories = 0


    def get_iteration_number(self, project):
        issue = self.jira.search_issues('project = ' + project +
                                        ' and "Iteration Planned" is not EMPTY ORDER BY "Iteration Planned" DESC',
                                        fields='customfield_10025', maxResults=1)[0]
        return issue.fields.customfield_10025.value


    def get_total_issues_count(self, project, iter):
        temp = self.jira.search_issues('project = ' + project + ' and "Iteration Planned" = ' + str(iter),
                                       fields='', maxResults=1, json_result=True)
        return temp['total']


    def get_issues(self, project, iter):
        return self.jira.search_issues('project = ' + project + ' and "Iteration Planned" = ' + str(iter),
                                       maxResults=self.get_total_issues_count(project, iter))


    def count_story_points(self, issues):

        for issue in issues:
            points = self.get_story_point(issue)
            status = str(issue.fields.status)
            if status == 'New' or status == 'Ready To Dev':
                self.ready_to_dev_points += points
                self.ready_to_dev_stories += 1
            elif status == 'In Dev':
                self.in_dev_points += points
                self.in_dev_stories += 1
            elif status == 'Ready To Test':
                self.ready_to_test_points += points
                self.ready_to_test_stories += 1
            elif status == 'In Test':
                self.in_test_points += points
                self.in_test_stories += 1
            elif status == 'Ready To Deliver':
                self.ready_to_deliver_points += points
                self.ready_to_deliver_stories += 1
            elif status == 'Archived':
                self.archived_points += points
                self.archived_stories += 1
            else:
                print 'ERROR!!! Wrong status of story'

            self.total_points = self.ready_to_dev_points + self.in_dev_points + \
                                self.ready_to_test_points + self.in_test_points + \
                                self.ready_to_deliver_points + self.archived_points
        return self.total_points


    def get_story_point(self, issue):
        point = issue.fields.customfield_10004
        if point != None:
            return int(point)
        return 0