import sys
import operator
from HTMLParser import HTMLParser
from flask import *
app = Flask(__name__)

parser = HTMLParser()

BASEURL = "http://www.google-melange.com/gci/org/google/gci2014/" \
    "{orgname}?fmt=json&limit=500&idx=1"

orglist = [
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


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/error')


@app.route('/error')
def error():
    return render_template('errors/404.html')


@app.route('/student/<name>-count=<int:e>-org=<org>')
def student(name, e=0, org=None):
    tasks = []
    code = 0
    interface = 0
    quality = 0
    doc = 0
    research = 0
    total = 0

    isAll = False
    if u'All' in org:
        isAll = True

    for orgname in orglist:
        page_json_f = open("orgs/%s.json" % orgname, "r")
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
        "student.html",
        tasks=tasks,
        total=total,
        code=code,
        interface=interface,
        quality=quality,
        documentation=doc,
        research=research,
        name=name,
        orgname=org)


@app.route('/org/<org>/')
def leaderboard(org):
    try:
        page_json_f = open("orgs/%s.json" % org, "r")
        page_json = json.loads(page_json_f.read())
        page_json_f.close()
    except:
        return redirect('/error')
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

    total = sum([int(tup[1]) for tup in final_dict.iteritems()])
    total_students = len(set([tup[0] for tup in final_dict.iteritems()]))
    return render_template("org.html", leaderboard=sorted_dict,
                           org=org,
                           total=total,
                           students=total_students,
                           code=code,
                           interface=interface,
                           quality=quality,
                           documentation=doc,
                           research=research,
                           )


@app.route('/all/')
def allorgs(draw=True):
    final_dict = {}

    current = 0
    totalorgs = {
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

    for org in orglist:
        page_json_f = open("orgs/%s.json" % org, "r")
        page_json = json.loads(page_json_f.read())
        page_json_f.close()
        data = page_json['data']['']
        for row in data:
            student_name = row['columns']['student']
            if student_name in final_dict:
                final_dict[student_name] += 1
            else:
                final_dict[student_name] = 1
            totalorgs[org][1] += 1
        current += 1

    sorted_dict = sorted(final_dict.iteritems(), key=lambda x: x[1],
                         reverse=True)
    total = sum([int(tup[1]) for tup in final_dict.iteritems()])
    total_students = len(set([tup[0] for tup in final_dict.iteritems()]))

    totalorgs = sorted(totalorgs.iteritems(), key=lambda x: x[0])
    return render_template("all.html", leaderboard=sorted_dict,
                           org="All Organizations",
                           total=total,
                           students=total_students,
                           totalorgs=totalorgs)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(sys.argv[1]))
