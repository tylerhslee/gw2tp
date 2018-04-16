#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Flask webapp
"""
import os

from flask import Flask, render_template, request
from json import dumps
from datetime import datetime, timedelta
from database import Session, Item, Listing
from dotenv import load_dotenv
from slack.authserver import authserver
from sqlalchemy.sql.expression import func, and_

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

envfile = os.path.join(BASE_DIR, '.env')
if os.path.isfile(envfile):
    load_dotenv(envfile)

session = Session()
app = Flask(__name__)
app.register_blueprint(authserver,
                       url_prefix='/slack')


def jsonify(data):
    # Assume the data always has ID, icon, name, prices, and margin columns
    ret = []
    for item in data:
        ret.append({'id': item.item_id,
                    'icon': item.icon,
                    'name': item.name,
                    'level': item.level,
                    's_price': item.s_price,
                    'b_price': item.b_price,
                    'p_margin': item.p_margin})
    return dumps(ret)


def find_lucrative():
    condition = ('listings.p_margin >= 0.2 AND ' +
                 'listings.p_margin < 1.0 AND ' +
                 'listings.supply > 800 AND ' +
                 'listings.demand > 800')
    days_from = datetime.now() - timedelta(days=1)
    cols = [Item.item_id, Item.icon, Item.name, Listing.s_price,
            Listing.b_price, Listing.p_margin, Listing.demand, Listing.supply,
            func.max(Listing.last_updated)]
    ret = (session.query(*cols)
           # Group by all cols in case there are duplicate values in other cols
           .group_by(*cols[:-1] + [Listing.last_updated])
           .join(Listing)
           .filter(condition,
                   and_(Listing.last_updated >= days_from))
           .order_by(Listing.last_updated.desc(), Listing.p_margin.desc()))
    return list(ret)[:10]


def find_item_from_name(name):
    cols = [Listing.item_id, Item.icon, Item.name, Item.level,
            Listing.s_price, Listing.b_price, Listing.p_margin,
            Listing.supply, Listing.demand,
            func.max(Listing.last_updated)]
    ret = (session.query(*cols)
           # Group by all cols in case there are duplicate values in other cols
           .group_by(*cols[:-1] + [Listing.last_updated])
           .join(Item)
           .filter('items.name="{n}"'.format(n=name))
           .order_by(Listing.last_updated.desc())
           .limit(1))
    return list(ret)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        featured = find_lucrative()
        return render_template('index.html', featured=featured)
    elif request.method == 'POST':
        results = find_item_from_name(request.form['item_name'])
        return render_template('index.html', featured=results)


@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        featured = find_lucrative()
        return jsonify(featured)
    elif request.method == 'POST':
        item_name = request.get_json()['item_name']
        results = find_item_from_name(item_name)
        return jsonify(results)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
