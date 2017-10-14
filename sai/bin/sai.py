import sys, json
import urllib2
import re

def url_decode(urlstring):
    return urllib2.unquote(urlstring).decode('utf8')

def decode_all_urls(messagestring):
    urlre = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.sub(urlre, decode_all_matching_urls, messagestring)

def decode_all_matching_urls(match):
    match = match.group()
    return url_decode(match)

def send_slack_message(settings):
    jtext = decode_all_urls(settings.get('message'))
    jusername = settings.get('from_user', 'Splunk')
    jurl = settings.get('from_user_icon')
    jcolor = settings.get('color')

    params = dict()
    params['attachments'] = []

    params['attachments'].append({'text': jtext,'username': jusername,'icon_url': jurl,'color': jcolor})

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