import sys
import json
import urllib2
import re
import csv
import gzip
import requests
import os

def url_decode(urlstring):
    return urllib2.unquote(urlstring).decode('utf8')

def decode_all_urls(messagestring):
    urlre = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.sub(urlre, decode_all_matching_urls, messagestring)

def decode_all_matching_urls(match):
    match = match.group()
    return url_decode(match)

def vertical_lines(row):
    for i, item in enumerate(row):
        if i != 0:
            row[i] = "| " + item

    return row

def write_csv(i, row):
    if i == 0:
        row.insert(0, 'row')
    else:
        row.insert(0, str(i))

    return row

def read_csv(file, settings):
    formatting = []
    output = []
    style = ""
    row_len = 0
    # gets column widths
    with gzip.open(file) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if settings.get("csv_row_numbers") == "1":
                row = write_csv(i, row)

            if settings.get("csv_v_break") == "1":
                row = vertical_lines(row)

            # Splunk appends an extra column for every result column that we do not need, we only want the first half
            for i, item in enumerate(row[:(len(row)/2)]):
                if (len(formatting) <= i): # inits the list
                    formatting.append(len(item) + 1)
                elif (formatting[i] < len(item) + 1):
                    formatting[i] = len(item) + 1
                else:
                    continue

        for value in formatting:
            row_len = value + row_len
            style = style + "{:<" + str(value) + "}"

    with gzip.open(file) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if settings.get("csv_row_numbers") == "1":
                row = write_csv(i, row)

            if settings.get("csv_v_break") == "1":
                row = vertical_lines(row)

            if i == 0:
                output.append("```")

            # horizontal lines
            if i == 1 and settings.get("csv_header_break") == "1":
                output.append("="*row_len)
            elif i > 1 and settings.get("csv_h_break") == "1":
                output.append("-"*row_len)
            else:
                pass

            formatted_row = (style.format(*row))
            output.append(formatted_row)

    output.append("```")
    return output

def screenshot(settings):
    if settings.get('screenshot') != "none":
        full_python = "python"

        if settings.get('panelrow') != None:
            panelrow = settings.get('panelrow')
        else:
            panelrow = ""
        # need access to selenium for screenshots
        command = full_python + " screenshot.py " + str(settings.get('dashboard')) + " " + str(settings.get('screenshot')) + " " + str(settings.get('channel')) + " " + str(settings.get('panelrow'))
        os.system(command)
    return

def format_fields(settings):
    if settings.get('assignee') == None:
        assignee = None
        pass
    elif ',' in settings.get('assignee') and settings.get('assignee_ping') == "1":
        contact = str(settings.get('assignee'))
        contacts = contact.split(',')
        assignee = "Primary: <" + contacts[0] + ">\nSecondary: <" + contacts[1] + ">"
    elif settings.get('assignee_ping') == "1":
        assignee = '<' + str(settings.get('assignee')) + '>'
    elif ',' in settings.get('assignee') and settings.get('assignee_ping') == "0":
        contact = str(settings.get('assignee'))
        contacts = contact.split(',')
        assignee = "Primary: " + contacts[0] + "\nSecondary: " + contacts[1]
    elif settings.get('assignee') != None:
        assignee = str(settings.get('assignee'))
    else: # multiple assignees and all should be pinged
        pass

    if settings.get('expected') != None:
        f1 = {'title': "Expected",'value': settings.get('expected'),'short': True}
    else: # no expected result given
        f1 = None

    if settings.get('actual') != None:
        f2 = {'title': "Actual",'value': settings.get('actual'),'short': True}
    else:
        f2 = None

    if assignee != None:
        f3 = {'title': "Assignee",'value': assignee,'short': True}
    else:
        f3 = None

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

    # Results Link is prepopulated
    f4 = {'title': "Links",'value': all_links,'short': True}

    return f1,f2,f3,f4

def send_slack_message(settings, global_settings):
    params = dict()
    heading = settings.get('heading')

    if settings.get('heading_bold') == "1":
        heading = '*' + heading + '*'

    if settings.get('heading_italic') == "1":
        heading = '_' + heading + '_'

    if settings.get('emoji') != None:
        params['text'] = str(settings.get('emoji')) + " " + heading
    else:
        params['text'] = heading

    params['username'] = settings.get('from_user', 'Splunk')
    params['icon_url'] = settings.get('from_user_icon')
    params['mrkdwn'] = True

    params['attachments'] = []
    if settings.get('author') != None:
        author = "Alert managed by: " + settings.get('author')

    if settings.get('csv') == "1":
        csv = read_csv(global_settings['results_file'], settings)
        csv = str(csv).replace("', '", "\n").replace("['", "").replace("']", "")
        text = str(settings.get('message'))
        text = text.replace('\\n', '\n')
        message = text + "\n\n" + csv
    else:
        message = str(settings.get('message'))
        message = message.replace('\\n', '\n')

    params['attachments'].append({'text': message,'color': settings.get('color'),'footer': author,'fields': format_fields(settings),"mrkdwn_in": ["text"]})

    # with open('data.json', 'w') as outfile:
    # 	json.dump(params, outfile)

    channel = settings.get('channel')
    if channel:
        params['channel'] = channel
    else:
        print >> sys.stderr, "WARN No channel supplied, using default for webhook"
    url = settings.get('webhook_url')
    body = json.dumps(params)
    print >> sys.stderr, 'DEBUG Calling url="%s" with body=%s' % (url, body)
    req = urllib2.Request(url, body, {"Content-Type": "application/json"})
    screenshot(settings)
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
        settings = payload
        config = payload.get('configuration')
        if not send_slack_message(config, settings):
            print >> sys.stderr, "FATAL Sending the slack message failed"
