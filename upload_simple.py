from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# loggin into the channel
channel = Channel()
channel.login("cl_s.json", "credentials.storage")

# setting up the video that is going to be uploaded
video = LocalVideo(file_path="./media/videos/1080p60/IterateColor.mp4")

# setting snippet
video.set_title("My Title")
video.set_description("This is a description")
video.set_tags(["this", "tag"])
video.set_category("gaming")
video.set_default_language("en-US")

# setting status
video.set_embeddable(True)
video.set_license("creativeCommon")
video.set_privacy_status("private")
video.set_public_stats_viewable(True)

# setting thumbnail
#video.set_thumbnail_path("test_thumb.png")
# video.set_playlist("PLDjcYN-DQyqTeSzCg-54m4stTVyQaJrGi")

# uploading video and printing the results
video = channel.upload_video(video)
print(video.id)
print(video)

# liking video
# video.like()