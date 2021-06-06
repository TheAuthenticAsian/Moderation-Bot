import os
from peewee import *
from dotenv import load_dotenv

# enviroment thing
load_dotenv()

db = SqliteDatabase('moderation_database.db')
# db = MySQLDatabase(os.getenv('database_name'), user=os.getenv('user'),
#                    password=os.getenv('password'), host=os.getenv('host'), port=os.getenv('port'))
db.connect()


class BaseModel(Model):
    username = CharField()
    user_id = IntegerField()

    class Meta:
        database = db


class KickedUser(BaseModel):
    kicked_by = TextField()
    date_kicked = DateField()
    reason = TextField()


class BannedUser(BaseModel):
    banned_by = TextField()
    date_banned = DateField()
    reason = TextField()


class WarnedUser(BaseModel):
    warned_by = TextField()
    date_warned = DateField()
    reason = TextField()


class MutedUser(BaseModel):
    muted_by = TextField()
    time_muted = DateTimeField()
    mute_time_release = DateTimeField()
    reason = TextField()


db.create_tables([KickedUser, BannedUser, WarnedUser, MutedUser])
db.close()
