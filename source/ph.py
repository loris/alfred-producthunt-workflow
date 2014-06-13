import json
import urllib2
import time
from xml.etree import ElementTree as ET


def get_items(uri, query=None):
    items = []
    data = json.loads(urllib2.urlopen(uri).read())
    sorted_data = sorted(data['hunts'], key=lambda k: k['votes'], reverse=True)
    for item in sorted_data:
        if 'permalink' in item:
            if query is None or query.lower() in item['title'].lower() or query.lower() in item['tagline'].lower():
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
        'uid': '%s%s' % (item['permalink'], time.time()),
        'arg': item['url'],
        'title': '%s - %s' % (item['title'], item['tagline']),
        'subtitle': '%s | %s | hunted by %s' % (plural(item['votes'], 'vote'), plural(item['comment_count'], 'comment'), item['user']['name']),
        'icon': 'icon.png'
    }

def plural(num=0, text=''):
    num = int(num)
    return '%d %s%s' % (num, text, 's'[num==1:])