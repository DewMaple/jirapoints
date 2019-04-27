# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template

from jirapointsweb import app
from jira_run import get_iter_result, jira_urp


default_project_name = "URP-BETA"
default_interator = 40

default_skype_list = ('aaa', 'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg', 'hhh')

# j_urp = jira_urp()


@app.route('/')
@app.route('/points', methods=['GET'])
def points():
    project_name = request.args.get('project_name', default=default_project_name, type=str)
    project_iterator = request.args.get('project_iterator', default=default_interator, type=int)
    skypelist = request.args.get('skypelist', default=default_skype_list, type=str)

    jira_urp.skype_list = skypelist
    jira_urp.current_iteration = project_iterator
    result = get_iter_result(self=jira_urp)
    print project_name, project_iterator, skypelist
    return render_template('points.html', project_name=project_name, result=result,
                           project_iterator=project_iterator, skypelist=skypelist)


@app.route('/send_points', methods=['GET'])
def send_points():
    project_name = request.args.get('project_name', default=default_project_name, type=str)
    project_iterator = request.args.get('project_iterator', default=default_interator, type=int)
    skypelist = request.args.get('skypelist', default=default_skype_list, type=str)

    jira_urp.skype_list = skypelist
    jira_urp.current_iteration = project_iterator
    result = get_iter_result(self=jira_urp)
    print result
    # daily_job(result)
    print "success!"
    return redirect(url_for('points'))

