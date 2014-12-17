import requests
import json

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

BASEURL = "http://www.google-melange.com/gci/org/google/gci2014/" \
    "{orgname}?fmt=json&limit=500&idx=1"


def update_orgs():
    print "Update started"
    for org in orglist:
        print org
        page_url = BASEURL.format(orgname=org)
        page = requests.get(page_url)
        data = page.json()
        f = open("orgs/%s.json" % org, "w")
        f.write(json.dumps(data))
        f.close()

    print "Updated."

update_orgs()
