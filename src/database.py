from peewee import *

db = SqliteDatabase('albums.db')


class BaseModel(Model):    
    class Meta:
        database = db

class Artist(BaseModel):
    name = CharField()

class Album(BaseModel):
    title = CharField()
    artist = ForeignKeyField(Artist, backref="albums")
    #mbid = CharField(unique=True)
    vote = IntegerField(default=0)
    favourite = BooleanField(default=False)


if not(db.table_exists([Album, Artist])):
    db.create_tables([Album, Artist])

#Album.insert(title="the wall", artist=Artist.create(name="pink floyd")).execute()

#rows = Album.select()
#print(rows.sql())
#for row in rows:
   #print ("title: {} artist: {}".format(row.title, row.artist.name))
#db.close()