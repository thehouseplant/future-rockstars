import datetime
import os
from random import *
from tinydb import TinyDB, Query

db_location = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'db.json'))
db = TinyDB(db_location)


def insert_member(form_body):
    first_name = form_body.getlist('firstName')[0]
    last_name = form_body.getlist('lastName')[0]
    gender = form_body.getlist('gender')[0]
    age = form_body.getlist('age')[0]
    street = form_body.getlist('street')[0]
    city = form_body.getlist('city')[0]
    state = form_body.getlist('state')[0]
    zip_code = form_body.getlist('zipCode')[0]
    phone = form_body.getlist('phone')[0]
    cohort = form_body.getlist('cohort')[0]
    talent = form_body.getlist('talent')[0]
    body = ({
        'memberId': randint(50, 500),
        'type': 'member',
        'firstName': first_name,
        'lastName': last_name,
        'gender': gender,
        'age': age,
        'street': street,
        'city': city,
        'state': state,
        'zipCode': zip_code,
        'phone': phone,
        'talent': talent,
        'cohort': cohort,
        'status': 'Submitted',
        'checkin': False,
        'forms': False,
        'payment': False
    })

    db.insert(body)


def query_by_type(query_type):
    entry = Query()
    return db.search(entry.type == query_type)


def query_member_by_id(member_id):
    member = Query()
    return db.search(member.memberId == member_id)


def remove_member_by_id(member_id):
    member = Query()
    db.remove(member.memberId == member_id)


def update_member_by_id(query, member_id):
    member = Query()
    db.update(query, member.memberId == member_id)


def close():
    db.close()
