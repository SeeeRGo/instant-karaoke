from flask import Flask
from transcribe import IterateColor
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import json
import urllib.parse
import ffmpeg
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# @app.route("/file-download")
# def hello_world():
#   load_dotenv()
#   scene = IterateColor("Kitty In A Casket - Cold Black Heart.mp3")
#   scene.render()
# 	return 'OK'
	# return send_file('./media/videos/1080p60/IterateColor.mp4', attachment_filename='python.mp4')

from flask import Flask, request, jsonify

ALLOWED_EXTENSIONS = set(['mp3', 'wav'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files.get('file')
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	artist = request.form.get('artist')
	name = request.form.get('name')
	lyrics = request.form.get('lyrics')
	if file and allowed_file(file.filename):
		file.save('./upload.wav')
		output_path = './output/accompaniment.wav'
		vocals_path = './output/vocals.wav'
		scene = IterateColor('./upload.wav', lyrics, output_path, vocals_path)
		scene.render()

		load_dotenv()
		url: str = os.environ.get("SUPABASE_URL")
		key: str = os.environ.get("SUPABASE_KEY")
		supabase: Client = create_client(url, key)

		video = ffmpeg.input('./media/videos/1080p60/IterateColor.mp4')
		audio = ffmpeg.input(output_path)
		out = ffmpeg.output(video, audio, './video.mp4', vcodec='copy', acodec='aac', strict='experimental')
		out.run(overwrite_output=True)
		audio = ffmpeg.input('./upload.wav')
		out = ffmpeg.output(video, audio, './video_edit.mp4', vcodec='copy', acodec='aac', strict='experimental')
		out.run(overwrite_output=True)
		file = open('./video.mp4','rb')
		upload_name = artist + ' - ' + name + '.mp4'
		res = supabase.storage.from_('file_queue').upload(upload_name, file)
		file_key = json.loads(res.read())['Key']
		file_url = url + '/storage/v1/object/public/' + urllib.parse.quote(file_key)
		file.close()
		file = open('./video_edit.mp4','rb')
		upload_name = artist + ' - ' + name + '_edit_version' '.mp4'
		res = supabase.storage.from_('file_queue').upload(upload_name, file)
		file_key = json.loads(res.read())['Key']
		file_edit_url = url + '/storage/v1/object/public/' + urllib.parse.quote(file_key)
		file.close()
		
		supabase.table('songs').insert({
			"name": name, 
			"artist": artist, 
			"timeline": scene.timeline,
			"link": file_url,
			"edit_link": file_edit_url
		}).execute()

		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are mp3'})
		resp.status_code = 400
		return resp
	
@app.route('/file-rerender', methods=['POST'])
def rerender_file():
	# check if the post request has the file part
	new_timeline = request.json['new_timeline']
	link = request.json['link']
	edit_link = request.json['edit_link']
	id = request.json['id']
	print(new_timeline, link, edit_link, id)
	resp = jsonify({'message' : 'File successfully uploaded'})
	resp.status_code = 201
	return resp
	# if 'file' not in request.files:
	# 	resp = jsonify({'message' : 'No file part in the request'})
	# 	resp.status_code = 400
	# 	return resp
	# file = request.files.get('file')
	# if file.filename == '':
	# 	resp = jsonify({'message' : 'No file selected for uploading'})
	# 	resp.status_code = 400
	# 	return resp
	# artist = request.form.get('artist')
	# name = request.form.get('name')
	# lyrics = request.form.get('lyrics')
	# if file and allowed_file(file.filename):
	# 	file.save('./upload.wav')
	# 	output_path = './output/accompaniment.wav'
	# 	vocals_path = './output/vocals.wav'
	# 	scene = IterateColor('./upload.wav', lyrics, output_path, vocals_path)
	# 	scene.render()

	# 	load_dotenv()
	# 	url: str = os.environ.get("SUPABASE_URL")
	# 	key: str = os.environ.get("SUPABASE_KEY")
	# 	supabase: Client = create_client(url, key)

	# 	video = ffmpeg.input('./media/videos/1080p60/IterateColor.mp4')
	# 	audio = ffmpeg.input(output_path)
	# 	out = ffmpeg.output(video, audio, './video.mp4', vcodec='copy', acodec='aac', strict='experimental')
	# 	out.run(overwrite_output=True)
	# 	audio = ffmpeg.input('./upload.wav')
	# 	out = ffmpeg.output(video, audio, './video_edit.mp4', vcodec='copy', acodec='aac', strict='experimental')
	# 	out.run(overwrite_output=True)
	# 	file = open('./video.mp4','rb')
	# 	upload_name = artist + ' - ' + name + '.mp4'
	# 	res = supabase.storage.from_('file_queue').upload(upload_name, file)
	# 	file_key = json.loads(res.read())['Key']
	# 	file_url = url + '/storage/v1/object/public/' + urllib.parse.quote(file_key)
	# 	file.close()
	# 	file = open('./video_edit.mp4','rb')
	# 	upload_name = artist + ' - ' + name + '_edit_version' '.mp4'
	# 	res = supabase.storage.from_('file_queue').upload(upload_name, file)
	# 	file_key = json.loads(res.read())['Key']
	# 	file_edit_url = url + '/storage/v1/object/public/' + urllib.parse.quote(file_key)

	# 	supabase.table('songs').insert({
	# 		"name": name, 
	# 		"artist": artist, 
	# 		"timeline": scene.timeline,
	# 		"link": file_url,
	# 		"edit_link": file_edit_url
	# 	}).execute()

	# 	resp = jsonify({'message' : 'File successfully uploaded'})
	# 	resp.status_code = 201
	# 	return resp
	# else:
	# 	resp = jsonify({'message' : 'Allowed file types are mp3'})
	# 	resp.status_code = 400
	# 	return resp