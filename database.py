# -*- coding: utf-8 -*-
"""
Interacts with the database for the web app.
"""
from yaml import load
from datetime import datetime
from sqlalchemy import create_engine, Column, ForeignKey, Integer, Float, \
    String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr

with open('./config.yml', 'r') as rf:
    config = load(rf)['sql-config']
    h = config['host']
    o = config['port']
    u = config['username']
    p = config['password']
    n = config['db']
    DATABASE_URL = 'mysql://{u}:{p}@{h}:{o}/{n}?charset=utf8' \
        .format(u=u, p=p, h=h, o=o, n=n)

Base = declarative_base()


def get_field(data, *args):
    keys = list(args)
    for k in keys:
        try:
            data = data[k]
        except KeyError:
            return None
    return data


def make_relation(name):
        return relationship(name, uselist=False, back_populates='item')


class ItemMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__tablename__

    @declared_attr
    def item_id(cls):
        return Column('item_id', ForeignKey('items.item_id'), primary_key=True)

    @declared_attr
    def item(cls):
        name = cls.__name__.lower()
        return relationship('Item', back_populates=name)


# NOTE: Request new data for minis
class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100))
    level = Column(Integer)
    rarity = Column(String(50))
    item_type = Column(String(50))
    icon = Column(String(500))

    # One-to-One relationships
    armor = make_relation('Armor')
    bag = make_relation('Bag')
    consumable = make_relation('Consumable')
    gatheringtool = make_relation('GatheringTool')
    gizmo = make_relation('Gizmo')
    salvagekit = make_relation('SalvageKit')
    trinket = make_relation('Trinket')
    upgrade = make_relation('Upgrade')
    weapon = make_relation('Weapon')

    # One-to-Many relationships
    listing = relationship('Listing', back_populates='item')

    @classmethod
    def create(cls, data):
        """Create an item object instance from raw JSON"""
        item = cls(item_id=data['id'],
                   name=data['name'],
                   level=data['level'],
                   rarity=data['rarity'],
                   item_type=data['type'],
                   icon=data['icon'])
        return item


class Armor(Base, ItemMixin):
    __tablename__ = 'armors'

    type = Column(String(50))
    defense = Column(Integer)
    weight_class = Column(String(50))

    @classmethod
    def create(cls, data):
        armor = cls(item_id=get_field(data, 'id'),
                    type=get_field(data, 'details', 'type'),
                    defense=get_field(data, 'details', 'defense'),
                    weight_class=get_field(data, 'details', 'weight_class'))
        return armor


class Bag(Base, ItemMixin):
    __tablename__ = 'bags'

    size = Column(Integer)
    is_safe = Column(Boolean)

    @classmethod
    def create(cls, data):
        bag = cls(item_id=get_field(data, 'id'),
                  size=get_field(data, 'details', 'size'),
                  is_safe=get_field(data, 'details', 'no_sell_or_sort'))
        return bag


class Consumable(Base, ItemMixin):
    __tablename__ = 'consumables'

    type = Column(String(50))
    duration = Column(Integer, nullable=True)

    @classmethod
    def create(cls, data):
        consumable = cls(item_id=get_field(data, 'id'),
                         type=get_field(data, 'details', 'type'),
                         duration=get_field(data, 'details', 'duration_ms'))
        return consumable


class GatheringTool(Base, ItemMixin):
    __tablename__ = 'gathering_tools'

    type = Column(String(50))

    @classmethod
    def create(cls, data):
        tool = cls(item_id=get_field(data, 'id'),
                   type=get_field(data, 'details', 'type'))
        return tool


class Gizmo(Base, ItemMixin):
    __tablename__ = 'gizmos'

    type = Column(String(50))

    @classmethod
    def create(cls, data):
        gizmo = cls(item_id=get_field(data, 'id'),
                    type=get_field(data, 'details', 'type'))
        return gizmo


class SalvageKit(Base, ItemMixin):
    __tablename__ = 'salvage_kits'

    type = Column(String(50))
    charges = Column(Integer)

    @classmethod
    def create(cls, data):
        kit = cls(item_id=get_field(data, 'id'),
                  type=get_field(data, 'details', 'type'),
                  charges=get_field(data, 'details', 'charges'))
        return kit


class Trinket(Base, ItemMixin):
    __tablename__ = 'trinkets'

    type = Column(String(50))

    @classmethod
    def create(cls, data):
        trinket = cls(item_id=get_field(data, 'id'),
                      type=get_field(data, 'details', 'type'))
        return trinket


class Upgrade(Base, ItemMixin):
    __tablename__ = 'upgrades'

    type = Column(String(50))

    @classmethod
    def create(cls, data):
        upgrade = cls(item_id=get_field(data, 'id'),
                      type=get_field(data, 'details', 'type'))
        return upgrade


class Weapon(Base, ItemMixin):
    __tablename__ = 'weapons'

    type = Column(String(50))
    min_power = Column(Integer)
    max_power = Column(Integer)
    defense = Column(Integer)
    damage_type = Column(String(50))

    @classmethod
    def create(cls, data):
        weapon = cls(item_id=get_field(data, 'id'),
                     type=get_field(data, 'details', 'type'),
                     min_power=get_field(data, 'details', 'min_power'),
                     max_power=get_field(data, 'details', 'max_power'),
                     defense=get_field(data, 'details', 'defense'),
                     damage_type=get_field(data, 'details', 'damage_type'))
        return weapon


class Listing(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), primary_key=False)
    demand = Column(Integer)                   # buy quantity
    supply = Column(Integer)                   # sell quantity
    b_price = Column(Integer)                  # buy price
    s_price = Column(Integer)                  # sell price
    p_margin = Column(Float, nullable=True)    # profit margin
    surplus = Column(Integer)                  # supply - demand
    last_updated = Column(DateTime)

    # Many-to-One relationships
    item = relationship('Item', back_populates='listing')

    @classmethod
    def create(cls, data):
        demand = int(get_field(data, 'buys', 'quantity'))
        supply = int(get_field(data, 'sells', 'quantity'))
        b_price = int(get_field(data, 'buys', 'unit_price'))
        s_price = int(get_field(data, 'sells', 'unit_price'))
        surplus = supply - demand
        if s_price:
            p_margin = (float(s_price) - b_price) / s_price
        else:
            p_margin = None

        return cls(item_id=get_field(data, 'id'),
                   demand=demand, supply=supply,
                   b_price=b_price, s_price=s_price,
                   p_margin=p_margin, surplus=surplus,
                   last_updated=datetime.now())


# Other function calls happen at the bottom for organization
engine = create_engine(DATABASE_URL, encoding='utf8', echo=False)
engine.connect()

# import Session, then initialize it with session = Session()
Session = sessionmaker(bind=engine)

# Create a new table if it doesn't already exist
Base.metadata.create_all(engine)
