#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update the item ID - name pairs in the database.
The GW2 API does not provide a native way to get item names from item IDs.

NOTE: Make sure the `items` database is always updated. Otherwise it will cause
`IntegrityError` in other scripts due to missing `item_id`s.
"""
from pprint import PrettyPrinter
from connector import API_KEY, Connector
from database import Session, Item, Armor, Bag, Consumable, GatheringTool, \
    Gizmo, SalvageKit, Trinket, Upgrade, Weapon

PAGE_SIZE = 200

pp = PrettyPrinter(indent=2)
session = Session()
connector = Connector(API_KEY)

# Number of valid pages for /items
g_max_page = connector.get_max_page('items')

# Tables
g_items = []
tables = [Armor, Bag, Consumable, GatheringTool, Gizmo,
          SalvageKit, Trinket, Upgrade, Weapon]
identity_sets = [[] for i in range(len(tables))]
g_pre_insert = list(zip(identity_sets, tables))  # [ ([], Armor), ... ]


def typeof(data, t):
    return data['type'] == t


def add(lst, data, table):
    new_data = [table.create(k) for k in data if typeof(k, table.__name__)]
    return lst + new_data


def update(min_page):
    global g_items
    global g_pre_insert

    print('\nRequesting from the API...')
    for page in range(min_page, g_max_page + 1):
        print('\rOn page %d/%d...' %
              (page - min_page, g_max_page - min_page), end='', flush=True)
        try:
            r = connector.get('items', params={'page': page,
                                               'page_size': PAGE_SIZE})
            data = r.json()
            g_items += [Item.create(k) for k in data]
            # Populate the identity sets => [ ([...], Armor), ... ]
            g_pre_insert = [(add(k[0], data, k[1]), k[1])
                            for k in g_pre_insert]
        except Exception:
            return page

    return None


def insert():
    print('\nInserting data into the database...')
    for ind, item in enumerate(g_items):
        print('\r{curr}/{tot}'.format(curr=ind, tot=len(g_items)),
              end='', flush=True)
        session.merge(item)

    for tup in g_pre_insert:
        for ind, row in enumerate(tup[0]):
            print('\r{name}: {curr}/{tot}'
                  .format(name=tup[1].__name__, curr=ind, tot=len(tup[0])),
                  end='', flush=True)
            session.merge(row)
        print('')

    session.commit()
    session.close()
    print('Done.')


def keep_trying():
    page = update(0)
    while page is not None:
        # Retry from the page that threw SSLError until it succeeds
        # Upperbound is set by the global variable max_page
        # TODO: Specify the error; right now it's caught by generic Exception
        print('\nSSLError. Trying again from page {p}...'.format(p=page))
        page = update(page)
    return True


if keep_trying():
    insert()
