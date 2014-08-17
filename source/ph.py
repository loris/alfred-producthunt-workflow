import json
import urllib2
import time
from xml.etree import ElementTree as ET


def get_items(uri, access_token, query=None):
    items = []
    request = urllib2.Request(uri)
    request.add_header('Authorization', 'Bearer '+ access_token)
    data = json.loads(urllib2.urlopen(request).read())
    # sorted_data = sorted(data['posts'], key=lambda k: k['votes_count'], reverse=True)
    for item in data['posts']:
        if 'id' in item:
            if query is None or query.lower() in item['name'].lower() or query.lower() in item['tagline'].lower():
                result = parse_item(item)
                items.append(result)

    xml = generate_xml(items)
    return xml


def generate_xml(items):
    xml_items = ET.Element('items')
    for item in items:
        xml_item = ET.SubElement(xml_items, 'item')
        for key in item.keys():
            if key is 'uid' or key is 'arg':
                xml_item.set(key, item[key])
            else:
                child = ET.SubElement(xml_item, key)
                child.text = item[key]
    print(ET.tostring(xml_items))


def parse_item(item):
    return {
        'uid': '%s%s' % (item['id'], time.time()),
        'arg': item['redirect_url'],
        'title': '%s - %s' % (item['name'], item['tagline']),
        'subtitle': '%s | %s | hunted by %s' % (plural(item['votes_count'], 'vote'), plural(item['comments_count'], 'comment'), item['user']['name']),
        'icon': 'icon.png'
    }

def plural(num=0, text=''):
    num = int(num)
    return '%d %s%s' % (num, text, 's'[num==1:])