#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from http.server import BaseHTTPRequestHandler,HTTPServer
import cgi
class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body>Hello Shivaansh!</body></html>"
            message += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            self.wfile.write(message.encode(encoding='utf_8'))
            print(message)
            return

        if self.path.endswith("/hola"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body> &#161 Hola ! </body></html>"
            message += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            message += "</body></html>"
            self.wfile.write(message.encode(encoding='utf_8'))
            print(message)
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
            try:
                length = int(self.headers['Content-Length'])
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                post_data = parse_qs(self.rfile.read(length).decode('utf-8'))
                messagecontent = post_data.get('name')[0].split('\n')[2]
                output = ''
                output += '<html><body>'
                output += '<h2> Okay, how about this: </h2>'
                output += '<h1> %s </h1>' % messagecontent
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text'><input type='submit' value='Submit'></form>"
                output += '</html></body>'
                self.wfile.write(output.encode('utf-8'))
            except:
                pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, stopping web server....")
        server.socket.close()

if __name__ == '__main__':
    main()
