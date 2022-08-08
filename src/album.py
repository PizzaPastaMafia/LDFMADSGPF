import requests
import json

class lastfm():
    def __init__(self, albumName, artistName):
        self.payload = {
            'method': 'album.getInfo',
            'artist': artistName,
            'album': albumName,
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

    def downloadCover(self):
        jsonData = self.lastfm_get(self.payload).json()
        url = jsonData['album']['image'][5]['#text']
        print(url)
        img_data = requests.get(url).content
        with open('pinkfloyd_darksideofthemoon.png', 'wb') as handler:
            handler.write(img_data)



#def jprint(obj):
    # create a formatted string of the Python JSON object
#    text = json.dumps(obj, sort_keys=True, indent=4)
#    print(text)

#r = lastfm.lastfm_get(lastfmpayload)
#r.status_code

#jprint(r.json())