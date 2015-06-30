from __future__ import unicode_literals
import subprocess
import time
import youtube_dl

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



def downld(self,txt):

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


	for v in videos:
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			for v in videos:
				self.send_header('Content-Disposition', 'attachment; filename=%s.mp3' % videos[v])
				self.end_headers()
				ydl.download([v])
				mp3  = open('./'+v+'.mp3', "r+").read()
				self.wfile.write(mp3)








