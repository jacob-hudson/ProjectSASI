import sys
import json
import urllib2
import re
import csv

def url_decode(urlstring):
    return urllib2.unquote(urlstring).decode('utf8')

def decode_all_urls(messagestring):
    urlre = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.sub(urlre, decode_all_matching_urls, messagestring)

def decode_all_matching_urls(match):
    match = match.group()
    return url_decode(match)

def screenshot():
    # TODO: create a bot user and use that uuser for the file API
    return

def format_fields(settings):
    f1 = {'title': "Expected",'value': settings.get('expected'),'short': True}
    f2 = {'title': "Actual",'value': settings.get('actual'),'short': True}
    f3 = {'title': "Assignee",'value': settings.get('asignee'),'short': True}

    links = []
    all_links = ""

    if settings.get('results') != None:
        links.insert(0,'<' + str(settings.get('results')) + '|Results>')

    if settings.get('dashboard') != None:
        links.insert(1,'<' + str(settings.get('dashboard')) + '|Dashboard>')

    if settings.get('trend') != None:
        links.insert(2,'<' + str(settings.get('trend')) + '|Trend>')

    if settings.get('playbook') != None:
        links.insert(3,'<' + str(settings.get('playbook')) + '|Playbook>')

    for link in links:
        if not link:
            continue
        else:
            if all_links == "":
                all_links = link + ' '
            else:
                all_links = all_links + '| ' + link + ' '

    f4 = {'title': "Links",'value': all_links,'short': True}
    return f1,f2,f3,f4

def send_slack_message(settings):
    params = dict()
    params['attachments'] = []
    author = "Alert managed by: " + settings.get('author')
    params['attachments'].append({'text': decode_all_urls(settings.get('message')),'pretext': settings.get('emoji') + settings.get('heading'),'username': settings.get('from_user', 'Splunk'),'icon_url': settings.get('from_user_icon'),'color': settings.get('color'),'author_name': author, 'fields': format_fields(settings)})



    with open('data.json', 'w') as outfile:
    	json.dump(params, outfile)

    channel = settings.get('channel')
    url = settings.get('webhook_url')
    body = json.dumps(params)
    print >> sys.stderr, 'DEBUG Calling url="%s" with body=%s' % (url, body)
    req = urllib2.Request(url, body, {"Content-Type": "application/json"})
    try:
        res = urllib2.urlopen(req)
        body = res.read()
        print >> sys.stderr, "INFO Slack API responded with HTTP status=%d" % res.code
        print >> sys.stderr, "DEBUG Slack API response: %s" % json.dumps(body)
        return 200 <= res.code < 300
    except urllib2.HTTPError, e:
        print >> sys.stderr, "ERROR Error sending message: %s" % e
        return False


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        payload = json.loads(sys.stdin.read())
        config = payload.get('configuration')
        if not send_slack_message(config):
            print >> sys.stderr, "FATAL Sending the slack message failed"
