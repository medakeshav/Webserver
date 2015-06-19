from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import threading
from SocketServer import ThreadingMixIn
class GetHandler(BaseHTTPRequestHandler):
	
	def Heders(self):
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
	
			"""GET"""
	def do_GET(self):
		if self.command == 'GET':
				if self.path =="/" or self.path == "/Login/index" or self.path == '/Login':
					Login()

				elif self.path == '/city1.jpg':
					img  = open("./Login/city1.jpg", "r+").read()
					self.wfile.write(img)

				elif self.path == '/favicon.ico':
					pass
					
				else:
					Show  = open("./Login/"+self.path, "r+").read()
					self.wfile.write(Show)
		self.send_response(200)
		self.end_headers()
		print "Active Threads: "+str(threading.active_count())
		print "Current Thread: "+str(threading.current_thread())
		print "List of Threads:"+str(threading.enumerate())

			"""Post"""
	def do_POST(self):
		if self.command == 'POST':
			if self.path == "/myform":
				Form()
				self.send_response(200)
				self.send_header("Content-type", "text/html")
				self.end_headers()
				print "Active Threads: "+str(threading.active_count())
				print "Current Thread: "+str(threading.current_thread())
				print "List of Threads:"+str(threading.enumerate())

			"""For Dynamic Pages"""
	def Login(self):
		Login  = open("./Login/index.html", "r+").read()
		self.wfile.write(Login)

	def From(self):
		length = int(self.headers['Content-Length'])
		post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
		username =  str(post_data['user'][0])
		password =  str(post_data['password'][0])
		From  = open("./Login/form.html", "r+").read()
		Form = Form % (username,password)
		self.wfile.write(Form)

		"""Threading"""

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

    	"""Serve"""
if __name__ == '__main__':
	print "Active Threads: "+str(threading.active_count())
	print "Current Thread: "+str(threading.current_thread())
	print "List of Threads:"+str(threading.enumerate())
	server = ThreadedHTTPServer(('localhost', 8080), GetHandler)
	print ('Starting server, use <Ctrl-C> to stop')	
	server.serve_forever()
