from googleapiclient.discovery import build


class Request_Maker:
    def search_song(self,search):
        youtube_key = 'AIzaSyC5U5fP5mTI_dpNDJn4wCr9QPe5ulpdRHI'
        search_music = search.get().strip().split()
        key = ''
        for i in range(len(search_music)):
            if i!=len(search_music)-1:
                word = search_music[i] + '+'
                key += word
            else : key+=search_music[i]
        # Creating the search object
        youtube = build('youtube', 'v3', developerKey=youtube_key)
        request = youtube.search().list(
            part="snippet",
            q=key,
            maxResults=50,
        )
        return request