import requests
import json
import os

try:
    os.mkdir("gci2012")
except:
    pass

orglist = [
    'apertium',
    'brlcad',
    'copyleftgames',
    'haiku',
    'kde',
    'rtems',
    'sahana',
    'sugarlabs2012',
    'fedora',
    'netbsd']

BASEURL = "http://www.google-melange.com/gci/org/google/gci2012/" \
    "{orgname}?fmt=json&limit=1000&idx=1"


def update_orgs():
    print "Update started"
    for org in orglist:
        print org
        page_url = BASEURL.format(orgname=org)
        page = requests.get(page_url)
        data = page.json()
        f = open("gci2012/%s.json" % org, "w")
        f.write(json.dumps(data))
        f.close()

    print "Updated."
    os.remove("updating")

f = open("updating", "w")
f.close()
update_orgs()
