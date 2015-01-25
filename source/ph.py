#!/usr/bin/python
# encoding: utf-8

import sys
import time

from workflow import ICON_WARNING, web, Workflow

log = None

def get_posts():
    response = web.get('https://alfred-producthunt-workflow.herokuapp.com/v1/posts').json()
    return response['posts']

def plural(num=0, text=''):
    num = int(num)
    return '%d %s%s' % (num, text, 's'[num==1:])

def main(wf):

    posts = wf.cached_data('posts', get_posts, max_age=60)

    if posts:
        for post in posts:
            wf.add_item(
                '%s - %s' % (post['name'], post['tagline']),
                '%s | %s | hunted by %s' % (plural(post['votes_count'], 'vote'), plural(post['comments_count'], 'comment'), post['user']['name']),
                arg=post['redirect_url'],
                valid=True,
                icon=u'icon.png',
                uid=u'%s%s' % (post['id'], time.time())
            )
    else:
        wf.add_item('No items', icon=ICON_WARNING)

    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'loris/alfred-producthunt-workflow',
        'version': '1.0',
        'frequency': 1
    })

    if wf.update_available:
        wf.start_update()

    log = wf.logger
    sys.exit(wf.run(main))