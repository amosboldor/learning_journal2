"""."""

import os
import sys
import transaction
from datetime import datetime

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)

from ..models import Entries


def usage(argv):
    """."""
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    """."""
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        for entry in ENTRIES:
            row = Entries(title=entry['title'], title1=entry['title1'], create_date=entry['create_date'], body=entry['body'])
            dbsession.add(row)


ENTRIES = [
    {'title': 'Week 2', 'title1': 'Day 5', 'create_date': datetime.strptime('December 18, 2016', '%B %d, %Y'), 'body': 'Cherries are rotten'},
    {'title': 'Week 3', 'title1': 'Day 1', 'create_date': datetime.strptime('December 19, 2016', '%B %d, %Y'), 'body': 'Apples are rotten'},
    {'title': 'Week 3', 'title1': 'Day 2', 'create_date': datetime.strptime('December 20, 2016', '%B %d, %Y'), 'body': 'Oranges are rotten'},
    {'title': 'Week 3', 'title1': 'Day 3', 'create_date': datetime.strptime('December 21, 2016', '%B %d, %Y'), 'body': 'Kiwis are rotten'},
    {'title': 'Week 3', 'title1': 'Day 4', 'create_date': datetime.strptime('December 22, 2016', '%B %d, %Y'), 'body': 'Mangos are rotten'},
    {'title': 'Week 3', 'title1': 'Day 5', 'create_date': datetime.strptime('December 23, 2016', '%B %d, %Y'), 'body': 'Pomogranets are rotten'}
]
