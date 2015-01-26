import sys
import json
import os
from HTMLParser import HTMLParser
from flask import *
app = Flask(__name__)
import subprocess
parser = HTMLParser()

BASEURL = "http://www.google-melange.com/gci/org/google/gci2014/" \
    "{orgname}?fmt=json&limit=1000&idx=1"

orglist2014 = [
    'apertium',
    'brlcad',
    'copyleftgames',
    'drupal',
    'fossasia',
    'haiku',
    'kde',
    'mifos',
    'openmrs',
    'sahana',
    'sugarlabs',
    'wikimedia']

orglist2013 = [
    'apertium',
    'brlcad',
    'copyleftgames',
    'drupal',
    'haiku',
    'kde',
    'rtems',
    'sahana',
    'sugarlabs2013',
    'wikimedia']

orglist2012 = [
    'apertium',
    'brlcad',
    'copyleftgames',
    'haiku',
    'kde',
    'rtems',
    'sahana',
    'fedora',
    'sugarlabs2012',
    'netbsd']


def get_tasks(
        page_json,
        code,
        interface,
        quality,
        doc,
        research,
        total):
    tasks = []
    data = page_json['data']['']
    for row in data:
        total += 1
        title = parser.unescape(row['columns']['title']).capitalize()
        link = "http://www.google-melange.com" + \
            row['operations']['row']['link']
        type_ = row['columns']['types']
        finalcat = []
        already = False

        if "Code" in type_:
            if not already:
                code += 1
                already = True
            type_short = 'Code'
            finalcat.insert(-1, type_short)

        if "Documentation" in type_:
            if not already:
                doc += 1
                already = True
            type_short = 'Documentation'
            finalcat.insert(-1, type_short)

        if "Research" in type_:
            if not already:
                research += 1
                already = True
            type_short = 'Outreach / Research'
            finalcat.insert(-1, type_short)

        if "Quality" in type_:
            if not already:
                quality += 1
                already = True
            type_short = 'Quality Assurance'
            finalcat.insert(-1, type_short)

        if "User Interface" in type_:
            if not already:
                interface += 1
                already = True
            type_short = 'User Interface'
            finalcat.insert(-1, type_short)

        task = (title, link, finalcat)
        if task in tasks:
            continue
        tasks.append(task)

    return code, interface, quality, doc, research, total


@app.route('/gitpull')
def gitpull():
    subprocess.Popen(["git", "pull", "--force"])
    return redirect('/')


@app.route('/')
def start_index():
    return redirect('/gci2014')


@app.route('/<year>/')
def index(year='gci2014'):
    return render_template('%s/index.html' % year)


@app.errorhandler(404)
def page_not_found(e):
    return redirect('gci2014/error')


@app.route('/<year>/error')
def error(year):
    return render_template('%s/errors/404.html' % year)

currentprocess = None


@app.route('/<year>/update/org/<orgname>')
def update(year, orgname):
    global currentprocess
    if currentprocess:
        currentprocess.terminate()
        currentprocess = None

    f = open("updating", "w")
    f.close()

    if year == 'gci2013':
        script = 'update2012.py'
    elif year == 'gci2013':
        script = 'update2013.py'
    else:
        script = 'update2014.py'

    currentprocess = subprocess.Popen(["python", script])
    if orgname == 'all':
        link = '%s/all' % year
    else:
        link = '%s/org/%s' % (year, orgname)
    return redirect(link)


@app.route('/<year>/student/<name>', defaults={'org': u'All Organizations'})
@app.route('/<year>/student/<name>/<org>')
def student(year, name, org=u'All'):
    tasks = []
    code = 0
    interface = 0
    quality = 0
    doc = 0
    research = 0
    total = 0

    isAll = u'All' in org

    if year == 'gci2012':
        orglist = orglist2012
    elif year == 'gci2013':
        orglist = orglist2013
    else:
        orglist = orglist2014

    for orgname in orglist:
        page_json_f = open("%s/%s.json" % (year, orgname), "r")
        page_json = json.loads(page_json_f.read())
        page_json_f.close()

        data = page_json['data']['']
        for row in data:
            student_name = row['columns']['student']
            if student_name == name and (isAll or orgname == org):
                total += 1
                student_name = row['columns']['student']
                title = parser.unescape(row['columns']['title']).capitalize()
                link = "http://www.google-melange.com" + \
                    row['operations']['row']['link']
                type_ = row['columns']['types']
                finalcat = []
                already = False

                if "Code" in type_:
                    if not already:
                        code += 1
                        already = True
                    type_short = 'Code'
                    finalcat.insert(-1, type_short)

                if "Documentation" in type_:
                    if not already:
                        doc += 1
                        already = True
                    type_short = 'Documentation'
                    finalcat.insert(-1, type_short)

                if "Research" in type_:
                    if not already:
                        research += 1
                        already = True
                    type_short = 'Outreach / Research'
                    finalcat.insert(-1, type_short)

                if "Quality" in type_:
                    if not already:
                        quality += 1
                        already = True
                    type_short = 'Quality Assurance'
                    finalcat.insert(-1, type_short)

                if "User Interface" in type_:
                    if not already:
                        interface += 1
                        already = True
                    type_short = 'User Interface'
                    finalcat.insert(-1, type_short)

                task = (title, link, finalcat, orgname)
                if task in tasks:
                    continue
                tasks.append(task)

    tasks.sort()
    return render_template(
        "%s/student.html" % year,
        tasks=tasks,
        total=total,
        code=code,
        interface=interface,
        quality=quality,
        documentation=doc,
        research=research,
        name=name,
        orgname=org)


@app.route('/<year>/org/<org>/')
def leaderboard(org, year='gci2014'):
    try:
        page_json_f = open("%s/%s.json" % (year, org), "r")
        page_json = json.loads(page_json_f.read())
        page_json_f.close()
    except:
        return redirect('%s/error' % year)
    code = 0
    interface = 0
    quality = 0
    doc = 0
    research = 0
    total = 0
    code, interface, quality, doc, research, total = get_tasks(
        page_json, code, interface, quality, doc, research, total)

    final_dict = {}

    data = page_json['data']['']
    for row in data:
        student_name = row['columns']['student']
        if student_name in final_dict:
            final_dict[student_name] += 1
        else:
            final_dict[student_name] = 1

    sorted_dict = sorted(final_dict.iteritems(), key=lambda x: x[1],
                         reverse=True)

    is_updating = os.path.exists("updating")
    total = sum([int(tup[1]) for tup in final_dict.iteritems()])
    total_students = len(set([tup[0] for tup in final_dict.iteritems()]))
    return render_template("%s/org.html" % year, leaderboard=sorted_dict,
                           org=org,
                           total=total,
                           students=total_students,
                           code=code,
                           interface=interface,
                           quality=quality,
                           documentation=doc,
                           research=research,
                           updating=is_updating)


@app.route('/<year>/all/')
def allorgs(year, draw=True):
    is_updating = os.path.exists("updating")
    final_dict = {}

    current = 0

    totalorgs2012 = {
        'apertium': ['Apertium', 0],
        'brlcad': ['BRL-CAD', 0],
        'copyleftgames': ['Copyleft Games', 0],
        'sugarlabs2012': ['Sugar Labs', 0],
        'haiku': ['Haiku', 0],
        'kde': ['KDE', 0],
        'rtems': ['RTEMS Project', 0],
        'sahana': ['Sahana Eden', 0],
        'fedora': ['Fedora', 0],
        'netbsd': ['NetBSD', 0]}

    totalorgs2013 = {
        'apertium': ['Apertium', 0],
        'brlcad': ['BRL-CAD', 0],
        'copyleftgames': ['Copyleft Games', 0],
        'drupal': ['Drupal', 0],
        'haiku': ['Haiku', 0],
        'kde': ['KDE', 0],
        'rtems': ['RTEMS Project', 0],
        'sahana': ['Sahana Eden', 0],
        'sugarlabs2013': ['Sugar Labs', 0],
        'wikimedia': ['Wikimedia', 0]}

    totalorgs2014 = {
        'apertium': ['Apertium', 0],
        'brlcad': ['BRL-CAD', 0],
        'copyleftgames': ['Copyleft Games', 0],
        'drupal': ['Drupal', 0],
        'fossasia': ['FOSS Asia', 0],
        'haiku': ['Haiku', 0],
        'kde': ['KDE', 0],
        'mifos': ['Mifos', 0],
        'openmrs': ['OpenMRS', 0],
        'sahana': ['Sahana Eden', 0],
        'sugarlabs': ['Sugar Labs', 0],
        'wikimedia': ['Wikimedia', 0]}

    if year == 'gci2014':
        orgsforyear = totalorgs2014
    elif year == 'gci2013':
        orgsforyear = totalorgs2013
    elif year == 'gci2012':
        orgsforyear = totalorgs2012
    else:
        return redirect('%s/error' % year)

    if year == 'gci2012':
        orglist = orglist2012
    elif year == 'gci2013':
        orglist = orglist2013
    else:
        orglist = orglist2014

    for org in orglist:
        try:
            page_json_f = open("%s/%s.json" % (year, org), "r")
            page_json = json.loads(page_json_f.read())
            page_json_f.close()
        except:
            return redirect('%s/error' % year)

        data = page_json['data']['']
        for row in data:
            student_name = row['columns']['student']
            if student_name in final_dict:
                final_dict[student_name] += 1
            else:
                final_dict[student_name] = 1
            orgsforyear[org][1] += 1
        current += 1

    sorted_dict = sorted(final_dict.iteritems(), key=lambda x: x[1],
                         reverse=True)
    total = sum([int(tup[1]) for tup in final_dict.iteritems()])
    total_students = len(set([tup[0] for tup in final_dict.iteritems()]))

    orgsforyear = sorted(orgsforyear.iteritems(), key=lambda x: x[0])
    return render_template("%s/all.html" % year, leaderboard=sorted_dict,
                           org="All Organizations",
                           total=total,
                           students=total_students,
                           totalorgs=orgsforyear,
                           updating=is_updating)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(sys.argv[1]))
