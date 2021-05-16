import vlc
import pafy

class Media_Maker:
    def media_maker(self,search_string):
        url = search_string
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        Instance = vlc.Instance()
        player = Instance.media_player_new()
        Media = Instance.media_new(playurl)
        Media.get_mrl()
        player.video_set_scale(0.001)
        player.set_media(Media)
        return player