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

    moderator = TextField()
    date = DateField()
    reason = TextField()

    class Meta:
        database = db


class KickedUser(BaseModel):
    pass


class BannedUser(BaseModel):
    pass


class UnbannedUser(BaseModel):
    pass


class WarnedUser(BaseModel):
    pass


class MutedUser(BaseModel):
    time_muted = DateTimeField()
    mute_time_release = DateTimeField()


db.create_tables([KickedUser, BannedUser, WarnedUser, MutedUser])
db.close()
