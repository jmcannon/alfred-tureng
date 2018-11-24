# encoding: utf-8

import sys
import urllib
from bs4 import BeautifulSoup
from workflow import Workflow3, web

BASE_URL = u'http://tureng.com/en/turkish-english/'
RESULTS_TABLE_CLASS = 'searchResultsTable'
ENGLISH_TERM_CLASS = 'en tm'
TURKISH_TERM_CLASS = 'tr ts'
CATEGORY_CLASS = 'hidden-xs'   # Must match exactly

def main(wf):
    query = wf.args[0]
    raw_url = BASE_URL + query
    url = urllib.quote(raw_url.encode('utf-8'), safe=":/")

    r = web.get(url)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find(class_=RESULTS_TABLE_CLASS)

    if table:
        categories = [x.get_text().strip() for x in table.find_all(lambda tag: tag.get('class') == [CATEGORY_CLASS])]
        target_terms = [x.get_text().strip() for x in table.find_all(class_=[ENGLISH_TERM_CLASS, TURKISH_TERM_CLASS])]

        category_index = 0
        for term in target_terms[1::2]:
            category = categories[category_index]
            subtitle = category if category != 'General' else ''
            wf.add_item(title=term, subtitle=subtitle, icon='icon.png', valid=True, arg=query)

            category_index += 1

    else:
        wf.add_item(title='No Match', valid=True, arg=query)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
