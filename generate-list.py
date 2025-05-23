#!/usr/bin/env python3

import json
import yattag
import sys

doc, tag, text = yattag.Doc().tagtext()

HEADER =\
'''
---
title: {}
---
'''

def format_entry(entry):
    '''
    Format an entry using dt as

    bolded title
    Author List
    Venue (if it exists), year
    buttons
    '''
    with tag('dt'):

        with tag('b'):
            text(entry['title'])

    with tag('dd'):
        with tag('div', klass="entry"):
            text(entry['authors'])

            if 'venue' in entry:
                doc.stag('br')
                with tag('em'):
                    text(entry['venue'])
                text(' ' + entry['year'])
            else:
                doc.stag('br')
                text(entry['year'])

            with tag('ul', klass='publinks'):
                for descr, link in entry['links'].items():
                    with tag('li'):
                        with tag('a', href=link):
                            text(descr)

with open(sys.argv[1]) as f:
    entries = json.load(f)

    target_file = entries[0]['file']
    title = entries[0]['title']

    with tag('dl', klass="ref"):
        for entry in entries[1:]:
            format_entry(entry)

    with open('content/{}.html'.format(target_file), 'w') as output:
        print(HEADER.format(title), file = output)
        print(yattag.indent(doc.getvalue(), indent_text = True), file = output)
