from youtube_client import YouTubeClient

def print_info_for_video(id):
    youtube_client = YouTubeClient()
    video = youtube_client.get_video_details(id)
    if video:
        video = video[0]
        response = youtube_client.youtube.videos().list(
            part="snippet,contentDetails,status",
            id=id
        ).execute()
        
        video_item = response['items'][0]
        duration = video_item['contentDetails']['duration']

        is_short = duration == 'PT60S' or duration.startswith('PT') and duration.endswith('S') and int(duration[2:-1]) <= 60

        print(f"Title: {video['snippet']['title']}")
        print(f"Description: {video['snippet']['description']}")
        print(f"Published at: {video['snippet']['publishedAt']}")
        print(f"Channel: {video['snippet']['channelTitle']}")
        print(f"Duration: {duration}")
        print(f"Is Short: {is_short}")
        print(video)
    else:
        print(f"Video with id {id} not found")
