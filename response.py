from googleapiclient.discovery import build

class Response:
    def response_func(self,request):
        response = request.execute()
        id_list = []
        desp_list = []
        for item in response['items']:
            try:
                id_list.append(str(item['id']['videoId']))
                desp_list.append([str(item['snippet']['title']), str(item['snippet']['channelTitle'])])
            except Exception :
                pass
        video_desp = dict(zip(id_list,desp_list))
        return video_desp,id_list