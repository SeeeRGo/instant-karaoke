from flask import Flask
from flask import send_file
from transcribe import IterateColor
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

app = Flask(__name__)

@app.route("/file-download")
def hello_world():
    scene = IterateColor("/project/01 - Bela Kiss.mp3")
    scene.render()
    # https://wkvsvhqxfoamibzzcrco.supabase.co/storage/v1/object/public/file_queue/Kitty%20In%20A%20Casket%20-%20Cold%20Black%20Heart.mp3?t=2023-08-19T08%3A32%3A53.964Z
    return send_file('./media/videos/1080p60/IterateColor.mp4', attachment_filename='python.mp4')

from flask import Flask, request, jsonify

ALLOWED_EXTENSIONS = set(['mp3'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		file.save('./upload.wav')
		scene = IterateColor('./upload.wav')
		scene.render()

		# loggin into the channel
		channel = Channel()
		channel.login("/project/client_secret.json", "/project/credentials.storage")

		# setting up the video that is going to be uploaded
		video = LocalVideo(file_path="./media/videos/1080p60/IterateColor.mp4")

		# setting snippet
		video.set_title("Test 2")
		video.set_description("This is a description")
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
		print('uploading now')
		# video = channel.upload_video(video)
		# print(video.id)
		# print(video)

		# liking video
# video.like()
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are mp3'})
		resp.status_code = 400
		return resp