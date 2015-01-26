import requests
import json
import os

try:
    os.mkdir("gci2013")
except:
    pass

orglist = [
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

BASEURL = "http://www.google-melange.com/gci/org/google/gci2013/" \
    "{orgname}?fmt=json&limit=1000&idx=1"


def update_orgs():
    print "Update started"
    for org in orglist:
        print org
        page_url = BASEURL.format(orgname=org)
        page = requests.get(page_url)
        data = page.json()
        f = open("gci2013/%s.json" % org, "w")
        f.write(json.dumps(data))
        f.close()

    print "Updated."
    os.remove("updating")

f = open("updating", "w")
f.close()
update_orgs()
