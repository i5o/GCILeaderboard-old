import sys
from HTMLParser import HTMLParser
from flask import *
app = Flask(__name__)

parser = HTMLParser()

BASEURL = "http://www.google-melange.com/gci/org/google/gci2014/" \
    "{orgname}?fmt=json&limit=500&idx=1"

orglist = ['sugarlabs',
           'mifos',
           'apertium',
           'brlcad',
           'sahana',
           'copyleftgames',
           'openmrs',
           'wikimedia',
           'kde',
           'haiku',
           'drupal',
           'fossasia']


@app.route('/')
def index():
    return render_template('index.html')


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

                if "User Interface" in type_:
                    interface += 1
                    type_ = 'User Interface'
                elif "Code" in type_:
                    code += 1
                    type_ = 'Code'
                elif "Quality" in type_:
                    quality += 1
                    type_ = 'Quality Assurance'
                elif "Documentation" in type_:
                    doc += 1
                    type_ = 'Documentation'
                elif "Research" in type_:
                    research += 1
                    type_ = 'Outreach / Research'

                task = (title, link, type_, orgname)
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
    page_json_f = open("orgs/%s.json" % org, "r")
    page_json = json.loads(page_json_f.read())
    page_json_f.close()

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
                           students=total_students)


@app.route('/all/')
def allorgs(draw=True):
    final_dict = {}

    current = 0
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
        current += 1

    sorted_dict = sorted(final_dict.iteritems(), key=lambda x: x[1],
                         reverse=True)
    total = sum([int(tup[1]) for tup in final_dict.iteritems()])
    total_students = len(set([tup[0] for tup in final_dict.iteritems()]))
    return render_template("org.html", leaderboard=sorted_dict,
                           org="All Organizations",
                           total=total,
                           students=total_students)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(sys.argv[1]))
