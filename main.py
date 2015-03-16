#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Google Code-In unofficial leaderboard
# Copyright (C) 2013-2015 Ignacio Rodríguez <ignacio@sugarlabs.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import os
import json
from utils import *
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request

app = Flask(__name__)
GCI = GCIUtils()


@app.route('/*')
def update_times():
    global TIMES_RELOADED
    if not os.path.exists("visits.json"):
        open("visits.json", "w").write("{}")

    TIMES_RELOADED = json.loads(open("visits.json", "r").read())
    if not request.path in TIMES_RELOADED:
        TIMES_RELOADED[request.path] = 1
    else:
        TIMES_RELOADED[request.path] += 1
    open("visits.json", "w").write(json.dumps(TIMES_RELOADED, indent=4))


@app.route('/gci<year>/', defaults={'year': str(CURRENT_CONTEST)})
@app.route('/gci<year>')
@app.route('/gci<year>/')
@app.route('/')
def start_index(year=CURRENT_CONTEST):
    update_times()
    return redirect('/gci' + str(year) + '/org/all')


@app.errorhandler(404)
def page_not_found(e):
    update_times()
    return render_template('errors/404.html', reloaded=TIMES_RELOADED)


@app.route('/org/<orgname>', defaults={'year': str(CURRENT_CONTEST)})
@app.route('/org/<orgname>/', defaults={'year': str(CURRENT_CONTEST)})
@app.route('/gci<year>/org/<orgname>')
@app.route('/gci<year>/org/<orgname>/')
def leaderboard_org(year, orgname):
    update_times()
    GCI.update_leaderboard(int(year))
    orgs = list(ORGS_DATA[int(year)]['orglist'])
    if orgname not in orgs:
        return page_not_found(404)

    pageOrgs = []
    for org in orgs:
        pageOrgs.append(
            {'id': org, 'name': GCI.get_org_name(int(year), org)})

    if orgname != 'all':
        totalTasks = len(ORG_TASKS[int(year)][orgname])
    else:
        totalTasks = 0
        for org in ORGS_DATA[int(year)]['orglist']:
            if org == 'all':
                continue
            totalTasks += len(ORG_TASKS[int(year)][org])

    org_title = GCI.get_org_name(int(year), orgname)
    tags = GCI.get_tasks_count(int(year), orgname)
    userTasks = sorted(
        CONTEST_LEADERBOARD[int(year)][orgname].iteritems(),
        key=lambda x: x[1]['tasks'],
        reverse=True)

    return render_template(
        'org.html',
        orgname=org_title,
        tags=tags,
        totalTasks=totalTasks,
        userTasks=userTasks,
        totalStudents=len(
            CONTEST_LEADERBOARD[int(year)][orgname]),
        org_id=orgname,
        orgs=pageOrgs,
        year=year,
        reloaded=TIMES_RELOADED[request.path])


@app.route('/loaded.json')
def loaded():
    return open('visits.json', 'r').read()


@app.route(
    '/student/<studentName>',
    defaults={
        'year': str(CURRENT_CONTEST),
        'org': u'all'})
@app.route('/gci<year>/student/<studentName>/<org>')
def student(year, studentName, org):
    update_times()
    studentTasks = GCI.get_student_tasks(studentName, int(year), org)
    tags = studentTasks['total_tags']

    orgs = list(ORGS_DATA[int(year)]['orglist'])
    pageOrgs = []
    for org_ in orgs:
        pageOrgs.append(
            {'id': org, 'name': GCI.get_org_name(int(year), org_)})

    studentTasks['tasks'] = sorted(studentTasks['tasks'].iteritems(),
                                   key=lambda x: x[1]['title'],
                                   reverse=False)

    if not studentTasks['tasks']:
        return render_template('errors/404.html')

    try:
        orgname = GCI.get_org_name(int(year), org)
    except KeyError:
        return render_template('errors/404.html')

    return render_template(
        'student.html',
        tags=tags,
        studentName=studentName,
        orgname=orgname,
        tasks=studentTasks['tasks'],
        year=year,
        orgs=pageOrgs,
        reloaded=TIMES_RELOADED[request.path])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(sys.argv[1]))
