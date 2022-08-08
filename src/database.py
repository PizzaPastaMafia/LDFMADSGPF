from peewee import *

db = SqliteDatabase('albums.db')

class Album(Model):
    title = CharField()
    artist = CharField()

    class Meta:
        database = db

#class Song(Model):
#    parent = ForeignKeyField(Album, backref='songs')
#    title = CharField()

#    class Meta:
#        database = db

db.connect()
db.create_tables([Album])
db.close()