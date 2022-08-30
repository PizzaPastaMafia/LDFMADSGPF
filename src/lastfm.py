import requests
import json
import re
import os

from database import *

class LastFm():
    payload = {
        'method': 'album.getInfo',
        'artist': '',
        'album': '',
    }

    def lastfm_get(self, payload):
        # define headers and URL
        headers = {'user-agent': 'Dataquest'}
        url = 'https://ws.audioscrobbler.com/2.0/'

        # Add API key and format to the payload
        self.payload['api_key'] = 'd8b9e3848409cbc83ec4a7d1f154fad5'
        self.payload['format'] = 'json'

        response = requests.get(url, headers=headers, params=self.payload)
        
        return response

    def getJson(self):
        return self.lastfm_get(self.payload).json()

    def toDatabase(self):
        db.connect()
        Album(title=self.getAlbumName, artist=self.getArtistName)
        #for song in self.getSongList():
        #    Song(Parent = self.getAlbumName, title = song)

        for album in Album.select():
            print(album.title)

        db.close()


    def downloadCover(self):
        jsonData = self.getJson()
        print(jsonData)
        url = jsonData['album']['image'][5]['#text']
        img_data = requests.get(url).content
        with open(os.path.join("../pics/", self.getImgName()), 'wb') as handler:
            handler.write(img_data)

    def setAlbumName(self, name):
        self.payload['album'] = name

    def setAlbumArtist(self, artist):
        self.payload['artist'] = artist

    def setAlbumInfo(self, name, artist):
        self.setAlbumName(name)
        self.setAlbumArtist(artist)

    def getSongList(self):
        jsonData = self.getJson()
        songList = []
        for song in jsonData['album']['tracks']['track']:
            songList.append(song['name'])
        print (songList)
        return songList

    def getSongByIndex(self, n):
        songList = self.getSongList()

        return songList[n]

    def getIndexOfSong(self, song):
        songList = self.getSongList()
        
        for s in songList:
            if s == song:
                return songList[s]
        
        return -1

    def getAlbumName(self):
        return self.payload['album']

    def getArtistName(self):
        return self.payload['artist']

    def getTrimmedAlbumName(self):
        return self.getAlbumName().replace(' ', '')

    def getTrimmedArtistName(self):
        return self.getArtistName().replace(' ', '')

    def getImgName(self):
        return self.getTrimmedAlbumName() + "_" + self.getTrimmedArtistName() + ".png"

    def getMbid(self):
        jsonData = self.getJson()
        return jsonData['album']['mbid']