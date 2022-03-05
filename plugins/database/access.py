# (c) @AbirHasan2005

from sample_config import Config
from plugins.database.database import Database

db = Database(Config.DATABASE_URL, Config.SESSION_NAME)
