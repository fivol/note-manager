from peewee import SqliteDatabase, Model, TextField, CharField, TimestampField, IntegerField

db = SqliteDatabase('sqlite_notes.db', autocommit=True, autorollback=True, autoconnect=True)


class NoteModel(Model):
    class Meta:
        database = db

    id = IntegerField(primary_key=True)
    name = CharField()
    body = TextField()
    date = IntegerField()


db.create_tables([NoteModel])
