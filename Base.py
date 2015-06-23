from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import threading
from SocketServer import ThreadingMixIn

def Login(self):
	filepath  = open("./public/login/index.html", "r+").read()
	self.wfile.write(filepath)

def Form(self):
	length = int(self.headers['Content-Length'])
	post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
	username =  str(post_data['user'][0])
	password =  str(post_data['password'][0])
	Form  = open("./views/form.html", "r+").read()
	Form = Form % (username,password)
	self.wfile.write(Form)

def public(self):
	try:
		public = open("./public/"+self.path, "r+").read()
		self.wfile.write(public)
	except IOError:
		self.wfile.write("Sorry This page does not exist")


Routes = {
	"/" : Login,
	"/myform" : Form,
	"/login" : Login,
	"/login/" : Login,
	"/login/index" : Login,
	"/login/index.html" : Login
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
		print "Active Threads: "+str(threading.active_count())
		print "Current Thread: "+str(threading.current_thread())
		print "List of Threads:"+str(threading.enumerate())

			#POST Request
	def do_POST(self):
		if self.command == 'POST':
				try:
					Routes[self.path](self)
				except KeyError:
					self.wfile.write("Sorry This page does not exist")

				self.send_response(200)
				self.send_header("Content-type", "text/html")
				self.end_headers()
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
	server = ThreadedHTTPServer(('localhost', 8080), GetHandler)
	print ('Starting server, use <Ctrl-Z> to stop')	
	server.serve_forever()
