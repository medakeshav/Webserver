from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import threading
from SocketServer import ThreadingMixIn

class GetHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		parsed_path = urlparse.urlparse(self.path)
		#print self.headers, self.path, self.command

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

		self.send_response(200)
		self.end_headers()

		if self.command == 'GET':
				if self.path =="/" or self.path == "/Login/index.html" or self.path == '/Login':
					Login  = open("./Login/index.html", "r+").read()
					self.wfile.write(Login)

				elif self.path == '/city1.jpg':
					img  = open("./Login/city1.jpg", "r+").read()
					self.wfile.write(img)

				elif self.path == '/favicon.ico':
					pass
					
				else:
					Show  = open("./Login/"+self.path, "r+").read()
					self.wfile.write(Show)
		print "Active Threads: "+str(threading.active_count())
		print "Current Thread: "+str(threading.current_thread())
		print "List of Threads:"+str(threading.enumerate())


	def do_POST(self):
		if self.command == 'POST':
			length = int(self.headers['Content-Length'])
			post_data = urlparse.parse_qs(self.rfile.read(length).decode('utf-8'))
			username =  str(post_data['user'][0])
			password =  str(post_data['password'][0])

			make = """<html>
		  <head>
		    <meta charset="UTF-8">


		    <title>Signin</title>
		    
		    
		       
		    
		        <script src="js/prefixfree.min.js"></script>

		    <link rel="stylesheet" href="css/flow.css">
		  </head>

		  <body background= "/city.jpg">

		    <div class="body"></div>
				<div class="grad"></div>
				<div class="header">
					<div>Welcome<span>Login</span></div><br>
					<div>Hi %s , welcome your account has been hacked
					Your password is %s </div>
				</div>
				<br>

			
				
		    <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
		  </body>
		</html> """	 % (username, password)

			self.wfile.write(make)

			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			print "Active Threads: "+str(threading.active_count())
			print "Current Thread: "+str(threading.current_thread())
			print "List of Threads:"+str(threading.enumerate())

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
	print "Active Threads: "+str(threading.active_count())
	print "Current Thread: "+str(threading.current_thread())
	print "List of Threads:"+str(threading.enumerate())
	server = ThreadedHTTPServer(('localhost', 8080), GetHandler)
	print ('Starting server, use <Ctrl-C> to stop')	
	server.serve_forever()