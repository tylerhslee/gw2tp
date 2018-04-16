#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Requests /commerce/prices for every listed item and saves that data to the
database along with other information.

NOTE: This script will throw an error regarding "foreign key constraint
failure". This error means that the `item_id` you are trying to add to the
database does not exist in the parent table (`items`). Make sure that the
parent table is updated if the error comes up.
"""
from datetime import datetime
from connector import API_KEY, Connector
from database import Session, Listing

from sqlalchemy.exc import IntegrityError

PAGE_SIZE = 200

session = Session()
connector = Connector(API_KEY)

# Number of valid pages for /commerce/prices
g_max_page = connector.get_max_page('commerce', 'prices')

# Tables
g_listings = []


def update(min_page):
    global g_listings

    print('\nRequesting from the API...')
    for page in range(min_page, g_max_page + 1):
        print('\rOn page %d/%d' %
              (page - min_page, g_max_page - min_page), end='', flush=True)
        try:
            r = connector.get('commerce', 'prices',
                              params={'page': page, 'page_size': PAGE_SIZE})
            data = r.json()
            g_listings += [Listing.create(k) for k in data]
        except Exception as e:
            return page

    return None


def insert():
    print('\n\nInserting data into the database...')
    for ind, listing in enumerate(g_listings):
        print('\r{curr}/{tot}'.format(curr=ind, tot=len(g_listings)),
              end='', flush=True)
        try:
            with session.begin_nested():
                session.add(listing)
        except IntegrityError as e:
            # Foreign key constraint error due to buggy items
            # TODO: Modify appropriately after the bug is addressed
            print('\nIntegrityError on Listing ID #{id}: skipping...'
                  .format(id=listing.item_id))
            pass
        except Exception as ee:
            raise ee

    session.commit()
    session.close()
    print('\nDone.')


def keep_trying():
    page = update(0)
    # Retry from the page that threw SSLError until it succeeds
    # Upperbound is set by the global variable max_page
    # TODO: Specify the error; right now it's caught by generic Exception
    while page is not None:
        print('\nSSLError. Trying again from page {p}...'.format(p=page))
        page = update(page)
    return True


if __name__ == '__main__':
    print('Running ' + __file__ + ' on ' + str(datetime.now()))
    if keep_trying():
        insert()
