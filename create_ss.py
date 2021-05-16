class Create_Search_String:
    def create_search_string(self,video_name,video_desp):
        search_string = ''
        print(video_desp)
        desp={}
        for id,name in video_desp.items():
            desp[name[0]] = id

        for name,id in desp.items():
            if name==video_name:
                search_string = 'https://www.youtube.com/watch?v=' + id
        return search_string
