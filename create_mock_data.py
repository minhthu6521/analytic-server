# -*- coding: utf-8 -*-

"""
Mock data

"""

import argparse
import random
import subprocess
import random

from sqlalchemy.exc import IntegrityError
from faker import Factory

from models.user_model import DEMO, ADMIN, RECRUITER, READER, HIRING_MANAGER, PILOT
from models.position_model import TEMPLATES, DRAFT, ACTIVE, EXPIRED, ARCHIVED,\
    DELETED, INACTIVE, PENDING, WAITING_FOR_APPROVAL, APPROVED
from models.application_model import APPLICANT_STATUSES, OUTCOME_STATUSES




def fake_email(i):
    fake = Factory.create("en")
    return u"{}{}-{}".format(i, random.randint(10000, 99999), fake.email())


def create_company(app, db, args):
    if args.seed:
        random.seed(args.seed)

    email = None
    if args.mail:
        if "@" not in args.mail:
            raise ValueError("No at in email address")
        email = args.mail.strip()

    if email is None:
        email = unicode(subprocess.check_output("git config --get user.email".split()).strip())
    emails = [email] + [fake_email(i) for i in xrange(args.main_users + 1)]

    templates = TEMPLATES.keys()
    mock_template = {
        "lang": "en",
        "main_email": email,
        "company": {
            "repeat": 1,
            "business_unit":{
                "repeat": 1
            },
            "user": {
                "repeat": args.main_users or 10,
                "email": emails,
                "role": [HIRING_MANAGER, READER, RECRUITER, ADMIN, DEMO],
                "job": {
                    "repeat": args.jobs or 20,
                    "template": templates,
                    "status": {DRAFT, ACTIVE, EXPIRED, APPROVED, PENDING},
                    "talent": {
                        "repeat": args.applicants or 10,
                        "talent_community": [True, False],
                        "confirmed_talent_community": [True, False],
                        "applicant": {
                            "repeat": 1,
                            "status": APPLICANT_STATUSES.keys(),
                            "outcome_status": [None] + OUTCOME_STATUSES.keys(),
                        }
                    }
                }
            },
            "talent": {
                "repeat": args.talents or 10,
                "talent_community": [True, False],
                "confirmed_talent_community": [True, False],
                "communities": ["developers", "sales", "operation", "customer"],
                "referral": {}
            }
        }
    }

    company_recipe = CompanyRecipe(app, mock_template, lang=args.lang, seed=args.seed or None)
    try:
        company = company_recipe.add_all(db, {})
    except IntegrityError, x:
        if 'Duplicate entry' in str(x.orig) and "for key 'email'" in str(x.orig):
            raise ValueError("Duplicate user email. Use -m parameter to use another one.")
        raise
    if args.events:
        add_demo_event_data(db, company[0])
    db.session.commit()
    print "Created company id: {}".format(company[0].id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, help="path to config file", required=True)
    parser.add_argument('-l', '--lang', type=str, help="language code (en, fi)", required=True)
    parser.add_argument('-s', '--seed', type=int, help="seed for repeatable faker", required=False)
    parser.add_argument('-m', '--mail', type=str, help="email for main user", required=False)
    parser.add_argument('--talents', type=int, help="Talents per user", required=False, default=0)
    parser.add_argument('--applicants', type=int, help="Applicants per job", required=False, default=10)
    parser.add_argument('--main-users', type=int, help="Main users", required=False, default=2)
    parser.add_argument('--subusers', type=int, help="Subusers", required=False, default=5)
    parser.add_argument('--jobs', type=int, help="Jobs per user", required=False, default=5)
    parser.add_argument('-e', '--events', help="Add some events", required=False, action='store_true')
    args = parser.parse_args()

    app = create_app(args.config)
    db = init_database(app)
    with app.app_context():
        create_company(app, db, args)
