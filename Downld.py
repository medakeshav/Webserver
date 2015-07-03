from __future__ import unicode_literals
import subprocess
#import time
from youtube_dl import YoutubeDL as ydl
import zipfile
from threading import Thread
import threading
from multiprocessing import Process

ydl_opts = {
	'format': 'best',
	'quite' : True,
	'verbose': False,
	'forcetitle' : True,
	'restrictfilenames': True,
	#'writethumbnail': True,
	'outtmpl': '%(id)s.%(ext)s',

	'postprocessors': [{
	'key': 'FFmpegExtractAudio',
	'preferredcodec': 'mp3',
	'preferredquality': '320'
	}]
}

def zipping_file(videos):
	 
	# loop through all the folders to zip
	z = zipfile.ZipFile("Music_File.zip", "w")
	for v in videos:
	    print("processing: " + videos[v])
	    z.write(v+".mp3")
	z.close()
	z = zipfile.ZipFile("Music_File.zip")
	z.printdir()



def video_download(handler,v,videos):
	
	try:
		ydl_opts['format'] = 'mp4'
		ydl(ydl_opts).download([v])
	except:
		ydl(ydl_opts).download([v])


	

def downld(handler,txt):

	videos = {}
	len = 0
	while txt.find('youtube.com',len) != -1:
	    len = txt.find('youtube.com',len+1)+12
	    if txt[len:len+5] == 'watch':
	    	key = txt[len+8:len+19]
	    	value = subprocess.Popen(['youtube-dl', '-q','-e',key,'--restrict-filenames'], stdout=subprocess.PIPE)
	    	out, err = value.communicate()
	    	videos[key] = out.strip().decode('ascii','ignore')
	    	print key
	    	

	len = 0

	while txt.find('youtu.be',len) != -1:
	    len = txt.find('youtu.be',len+1)+8
	    if txt[len:len+1] == '/':
			key = txt[len+1:len+12]
			value = subprocess.Popen(['youtube-dl', '-q','-e', key,'--restrict-filenames'], stdout=subprocess.PIPE)
			out, err = value.communicate()
			videos[key] = out.strip().decode('ascii','ignore')
			print key

	print videos
	if videos == '':
		#Msg_box = 
		#handler.wfile.write(Msg_box)
		exit(0)

	
	for v in videos:
		#global t
		v = Thread(target=video_download, args=(handler,v,videos))
		v.start()
	v.join()
		

	zipping_file(videos)
	
	mp3  = open('Music_File.zip', "r+")
	handler.send_response(200)
	handler.send_header('Content-Type', 'application/octet-stream')
	handler.send_header('Content-Disposition', 'attachment; filename=Music_File.zip')
	handler.end_headers()

	handler.wfile.write(mp3.read())
	mp3.close()






