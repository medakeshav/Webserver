from __future__ import unicode_literals
import subprocess
import time
from youtube_dl import YoutubeDL as ydl
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

def video_download(handler,v,videos):
	
	#handler.lock = threading.Lock()
	handler.send_header('Content-Disposition', 'attachment; filename=%s.mp3' % videos[v])
	try:
		ydl_opts['format'] = 'mp4'
		ydl(ydl_opts).download([v])
	except:
		ydl_opts['format'] = 'best'
		ydl(ydl_opts).download([v])		
	
	mp3  = open('./'+v+'.mp3', "r+").read()
	#handler.lock.acquire()
	handler.wfile.write(mp3)
	handler.end_headers()
	#handler.lock.release()


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

		p=Process(target=video_download, args=(handler,v,videos))
		p.start()
		p.join()











