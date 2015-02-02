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
from utils import *
from flask import Flask
from flask import render_template
from flask import redirect
app = Flask(__name__)
GCI = GCIUtils()


@app.route('/')
def start_index():
    return redirect('/org/all')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html')


@app.route('/org/<orgname>')
def leaderboard_org(orgname):
    GCI.update_leaderboard(CURRENT_CONTEST)
    orgs = list(ORGS_DATA[CURRENT_CONTEST]['orglist'])
    orgs.append('all')
    if orgname not in orgs:
        return page_not_found(404)

    if orgname != 'all':
        totalTasks = len(ORG_TASKS[CURRENT_CONTEST][orgname])
    else:
        totalTasks = 0
        for org in ORGS_DATA[CURRENT_CONTEST]['orglist']:
            totalTasks += len(ORG_TASKS[CURRENT_CONTEST][org])

    org_title = GCI.get_org_name(CURRENT_CONTEST, orgname)
    tags = GCI.get_tasks_count(CURRENT_CONTEST, orgname)
    userTasks = sorted(
        CONTEST_LEADERBOARD[CURRENT_CONTEST][orgname].iteritems(),
        key=lambda x: x[1]['tasks'],
        reverse=True)

    return render_template(
        'org.html',
        orgname=org_title,
        codeTasks=tags['Code'],
        userInterfaceTasks=tags['User Interface'],
        qualityAssuranceTasks=tags['Quality Assurance'],
        documentationTasks=tags['Documentation/Training'],
        outreachResearchTasks=tags['Outreach/Research'],
        totalTasks=totalTasks,
        userTasks=userTasks,
        totalStudents=len(
            CONTEST_LEADERBOARD[CURRENT_CONTEST][orgname]),
        org_id=orgname)


@app.route('/winners')
def winners():
    sortedWinners = sorted(
        WINNERS,
        key=lambda x: x[1],
        reverse=False)

    return render_template('winners.html', winners=sortedWinners)


@app.route('/student/<studentName>', defaults={'org': u'all'})
@app.route('/student/<studentName>/<org>')
def student(studentName, org):
    studentTasks = GCI.get_student_tasks(studentName, CURRENT_CONTEST, org)
    tags = studentTasks['total_tags']

    studentTasks['tasks'] = sorted(studentTasks['tasks'].iteritems(),
                                   key=lambda x: x[1]['title'],
                                   reverse=False)

    if not studentTasks['tasks']:
        return render_template('errors/404.html')

    try:
        orgname = GCI.get_org_name(CURRENT_CONTEST, org)
    except KeyError:
        return render_template('errors/404.html')

    return render_template(
        'student.html',
        codeTasks=tags['Code'],
        userInterfaceTasks=tags['User Interface'],
        qualityAssuranceTasks=tags['Quality Assurance'],
        documentationTasks=tags['Documentation/Training'],
        outreachResearchTasks=tags['Outreach/Research'],
        studentName=studentName,
        orgname=orgname,
        totalTasks=len(studentTasks['tasks']),
        tasks=studentTasks['tasks'],
        year=CURRENT_CONTEST)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(sys.argv[1]))
