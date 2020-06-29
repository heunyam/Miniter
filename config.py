db = {
    'user': 'root',
    'password': 'heunyam',
    'host': 'localhost',
    'port': 3306,
    'database': 'miniter'
}

# DB_URL = f"mysql+mysqlconnector://{db['user']:{db['password']}}@" \
#          f"{db['host']}:{db['port']}/{db['database']}?charset=utf8"

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
JWT_SECRET_KEY = 'secrete'
