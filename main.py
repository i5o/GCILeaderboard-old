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
import operator
from utils import *
from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import make_response

app = Flask(__name__)
GCI = GCIUtils()


@app.route('/gci<year>/', defaults={'year': str(CURRENT_CONTEST)})
@app.route('/gci<year>')
@app.route('/gci<year>/')
@app.route('/')
def start_index(year=CURRENT_CONTEST):
    return redirect('/gci' + str(year) + '/org/all')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html', reloaded=TIMES_RELOADED)


@app.route('/org/<orgname>', defaults={'year': str(CURRENT_CONTEST)})
@app.route('/org/<orgname>/', defaults={'year': str(CURRENT_CONTEST)})
@app.route('/gci<year>/org/<orgname>')
@app.route('/gci<year>/org/<orgname>/')
def leaderboard_org(year, orgname):
    org_title = GCI.get_org_name(int(year), orgname)
    tags = GCI.get_tasks_count(int(year), orgname)
    tasks = GCI.get_tasks(int(year), orgname)

    return render_template(
        'org.html',
        orgname=org_title,
        tags=tags,
        totalTasks=tasks["totalTasks"],
        userTasks=tasks["userTasks"],
        totalStudents=len(
            CONTEST_LEADERBOARD[int(year)][orgname]),
        org_id=orgname,
        orgs=tasks["pageOrgs"],
        year=year)


@app.route(
    '/student/<studentName>',
    defaults={
        'year': str(CURRENT_CONTEST),
        'org': u'all'})
@app.route('/gci<year>/student/<studentName>/<org>')
def student(year, studentName, org):
    studentTasks = GCI.get_student_tasks(studentName, int(year), org)
    tags = studentTasks['total_tags']
    tasks = GCI.get_tasks(int(year), org)

    studentPos = 1
    for x in tasks["userTasks"]:
        if x[1]['name'] == studentName:
            break
        studentPos += 1
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
        orgs=tasks["pageOrgs"],
        studentPos=studentPos)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(sys.argv[1]))
