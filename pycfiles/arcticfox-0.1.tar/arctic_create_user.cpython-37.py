# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/arctic/scripts/arctic_create_user.py
# Compiled at: 2019-02-02 17:02:31
# Size of source mod 2**32: 2321 bytes
import argparse, base64, logging, uuid
from pymongo import MongoClient
from arctic.arctic import Arctic
from .utils import do_db_auth
from ..hooks import get_mongodb_uri
logger = logging.getLogger(__name__)

def main():
    usage = "arctic_create_user --host research [--db mongoose_user] [--write] user\n\n    Creates the user's personal Arctic mongo database\n    Or add a user to an existing Mongo Database.\n    "
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('--host', default='localhost', help='Hostname, or clustername. Default: localhost')
    parser.add_argument('--db', default=None, help='Database to add user on. Default: mongoose_<user>')
    parser.add_argument('--password', default=None, help='Password. Default: random')
    parser.add_argument('--write', action='store_true', default=False, help="Used for granting write access to someone else's DB")
    parser.add_argument('users', nargs='+', help='Users to add.')
    args = parser.parse_args()
    c = MongoClient(get_mongodb_uri(args.host))
    if not do_db_auth(args.host, c, args.db if args.db else 'admin'):
        logger.error("Failed to authenticate to '%s'. Check your admin password!" % args.host)
        return
    for user in args.users:
        write_access = args.write
        p = args.password
        if p is None:
            p = base64.b64encode(uuid.uuid4().bytes).replace('/', '')[:12]
        db = args.db
        if not db:
            write_access = True
            db = Arctic.DB_PREFIX + '_' + user
        c[db].add_user(user, p, read_only=(not write_access))
        logger.info('Granted: {user} [{permission}] to {db}'.format(user=user, permission=('WRITE' if write_access else 'READ'),
          db=db))
        logger.info('User creds: {db}/{user}/{password}'.format(user=user, db=db,
          password=p))


if __name__ == '__main__':
    main()