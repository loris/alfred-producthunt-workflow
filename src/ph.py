#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import web, Workflow

log = None

def get_posts():
    url = 'https://alfred-producthunt-workflow.herokuapp.com/v1/posts'
    headers = {
        'user-agent': u'Alfred/%s.%s AlfredProductHuntWorkflow/%s/%s' % (
            wf.alfred_env.get('version'),
            wf.alfred_env.get('version_build'),
            wf.version,
            wf.alfred_env.get('workflow_uid')
        )
    }
    response = web.get(url, headers=headers).json()
    return response['posts']

def plural(num=0, text=''):
    num = int(num)
    return '%d %s%s' % (num, text, 's'[num==1:])

def main(wf):

    posts           = wf.cached_data('posts', get_posts, max_age=5*60)
    read_post_ids   = wf.stored_data('read_post_ids') or []
    displayed_posts = False

    if posts:
        for post in posts:
            if post['id'] not in read_post_ids:
                displayed_posts = True
                wf.add_item(
                    post['name'],
                    post['tagline'],
                    arg=u'open|%s|%s|%s' % (post['id'], post['redirect_url'], post['discussion_url']),
                    modifier_subtitles={
                        u'cmd': u'%s | %s | hunted by %s' % (plural(post['votes_count'], 'vote'), plural(post['comments_count'], 'comment'), post['user']['name'])
                    },
                    copytext=post['redirect_url'],
                    valid=True,
                    icon=u'link.png'
                )

    if displayed_posts:
        wf.add_item(
            u'Mark all as read',
            u'Hide above posts from now on',
            arg=u'mark_all_as_read',
            modifier_subtitles={
                u'cmd': u'Restore hidden posts'
            },
            valid=True,
            icon=u'check.png'
        )
    else:
        wf.add_item(
            u'No posts',
            u'Restore hidden posts',
            arg=u'mark_all_as_unread',
            modifier_subtitles={
                u'cmd': u'Restore hidden posts'
            },
            valid=True,
            icon=u'error.png'
        )

    wf.send_feedback()

def mark_all_as_read(wf):
    posts   = wf.cached_data('posts', get_posts, max_age=5*60)
    ids     = map(lambda x:x['id'], posts)

    wf.store_data('read_post_ids', ids)

def mark_all_as_unread(wf):
    wf.store_data('read_post_ids', None)

if __name__ == '__main__':
    wf = Workflow(update_settings={
        'github_slug': 'loris/alfred-producthunt-workflow',
        'version': '1.2',
        'frequency': 1
    })

    log     = wf.logger
    command = wf.args[0]

    if command == 'mark_all_as_read':
        sys.exit(wf.run(mark_all_as_read))
    elif command == 'mark_all_as_unread':
        sys.exit(wf.run(mark_all_as_unread))
    else:
        if wf.update_available:
            wf.start_update()
        sys.exit(wf.run(main))