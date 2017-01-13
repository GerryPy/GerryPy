"""Initialize the database with the District table."""

import os
import sys
import transaction
from pyramid.paster import (
    get_appsettings,
    setup_logging
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session)
from ..models import District


def usage(argv): #pragma: no cover
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):#pragma: no cover
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

        model = District(district_number=1, area=345.3, population=5000)
        dbsession.add(model)
