class DisplayResults:
    def display_results(self,video_desp,id_list):
        video_name_list = []
        for item in id_list:
            video_name_list.append(video_desp[item])
        return video_name_list