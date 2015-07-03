from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer 
import urlparse
import threading
from SocketServer import ThreadingMixIn, ForkingMixIn
from Downld import *



def Login(handler):	
	filepath  = open("./public/login/index.html", "r+").read()
	handler.wfile.write(filepath)

def Form(handler):
	length = int(handler.headers['Content-Length'])
	post_data = urlparse.parse_qs(handler.rfile.read(length).decode('utf-8'))
	username =  str(post_data['user'][0])
	password =  str(post_data['password'][0])	
	Form  = open("./views/form.html", "r+").read()
	Form = Form % (username)
	handler.wfile.write(Form)

def file_dl(handler):
	length = int(handler.headers['Content-Length'])
	txt = str(handler.rfile.read(length).decode("ascii", "ignore"))
	fp =open('./sample.txt','w+')
	fp.write(txt)
	fp.close()
	downld(handler,txt)


def public(handler):
	try:
		print handler.path
		public = open("./public"+handler.path, "r+").read()
		handler.wfile.write(public)
	except IOError:
		handler.wfile.write("Sorry This page does not exist")
	handler.send_header("Content-type", "text/html")

Routes = {
	"/" : Login,
	"/myform" : Form,
	"/login" : Login,
	"/login/" : Login,
	"/login/index" : Login,
	"/login/index.html" : Login,
	"/upload" : file_dl,
	"/url": file_dl
	}

class GetHandler(BaseHTTPRequestHandler):

		#Supplying Header information
	def Headers(self):
		parsed_path = urlparse.urlparse(self.path)
		message_parts = [
			'CLIENT VALUES:',
			'client_address=%s (%s)' % (self.client_address,
			                            self.address_string()),
			'command=%s' % self.command,
			'path=%s' % self.path,
			'real path=%s' % parsed_path.path,
			'query=%s' % parsed_path.query,
			'request_version=%s' % self.request_version,
			'',
			'SERVER VALUES:',
			'server_version=%s' % self.server_version,
			'sys_version=%s' % self.sys_version,
			'protocol_version=%s' % self.protocol_version,
			'',
			'HEADERS RECEIVED:',
			]
		print message_parts, self.headers


			#GET Request
	def do_GET(self):
		if self.command == 'GET':
			try:
				Routes[self.path](self)
			except KeyError:
				public(self)
			self.send_response(200)
			self.end_headers()
		Thread_status()

			#POST Request
	def do_POST(self):
		if self.command == 'POST':
			try:
				Routes[self.path](self)
			except KeyError:
				public(self)
			self.send_response(200)
			self.end_headers()
			Thread_status()
	
	def Thread_status(self):
		print "Active Threads: "+str(threading.active_count())
		print "Current Thread: "+str(threading.current_thread())
		print "List of Threads:"+str(threading.enumerate())

			#Threading
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

    		#Serve
if __name__ == '__main__':
	print "Active Threads: "+str(threading.active_count())
	print "Current Thread: "+str(threading.current_thread())
	print "List of Threads:"+str(threading.enumerate())
	server = ThreadedHTTPServer(('0.0.0.0', 8080), GetHandler)
	print ('Starting server, use <Ctrl-Z> to stop')	
	server.serve_forever()
