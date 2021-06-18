import os
from peewee import *
from dotenv import load_dotenv

# environment thing
load_dotenv()

#db = SqliteDatabase('moderation_database.db')
db = MySQLDatabase(os.getenv('database_name'), user=os.getenv('user'),
                   password=os.getenv('password'), host=os.getenv('host'), port=int(os.getenv('port')))
db.connect()


class BaseModel(Model):
    id = AutoField()
    username = CharField()
    user_id = BigIntegerField()

    moderator_id = TextField()
    date = DateField()
    reason = TextField()

    class Meta:
        database = db


class ModerationLogs(BaseModel):
    action = TextField()


class MutedUser(BaseModel):
    time_muted = DateTimeField()
    mute_time_release = DateTimeField()


if __name__ == "__main__":
    models = BaseModel.__subclasses__()
    db.create_tables(models)
    db.close()
