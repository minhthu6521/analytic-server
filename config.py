SQLALCHEMY_DATABASE_URI = 'mysql://root:salasana@localhost/Analytics?charset=utf8mb4'
PRODUCTION = False
FETCH_URL = "http://localhost:5000/api/vra-data?from={date}"
HASH_SALT = "randomsalt"
HASH_MIN_LENGTH = 3
SQLALCHEMY_TRACK_MODIFICATIONS = False