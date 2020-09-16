#!/usr/bin/python
# -*- coding: utf-8 -*-
# Webserver imports

from http.server import BaseHTTPRequestHandler,HTTPServer
import cgi

# SQL ALchemy imports

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()


                restaurants = session.query(Restaurant).all()



                output = '<html><body>'
                output += \
                    '<h2><a href = "/restaurants/new">Make a New Restaurant Here</a></h2>'

                for restaurant in restaurants:
                    output += '<h2>%s<h2>' % restaurant.name
                    output += \
                        "<ul><li><a href = '/restaurants/%s/edit'>Edit</a></li>" \
                        % restaurant.id
                    output += \
                        "<li><a href = 'restaurants/%s/delete'>Delete</a></li></ul>" \
                        % restaurant.id

                    # print output # for debugging

                output += '</body></html>'
                self.wfile.write(output.encode(encoding='utf_8'))

                return   # exit if statement
            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = '<html><body>'
                output += \
                '''<form method = 'POST' enctype='multipart/form-data' action='/restaurants/new'>Name of Restaurant<input name = "message" type = "text" placeholder = 'New Restaurant Name'><input type = "submit" value="Submit" ></form>'''
                output += '</body></html>'

                #output += '''<form method = 'POST' enctype='multipart/form-data' action='/restaurants/create'>Name of Restaurant<input name = "message" type = "text"><input type = "submit" value="Submit"></form>'''

                self.wfile.write(output.encode(encoding='utf_8'))
                return

        except:
            pass

    def do_POST(self):
        try:
            if self.path.endswith('restaurants/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messagecontent = fields.get('message')
                    newRestaurant = Restaurant(name = '%s' % messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


                    output = '<html><body>'
                    output += 'Restaurant has been added to the database! Please go back to '
                    output += '<a href = /restaurants>Restaurants List</a>'
                    output += "</html></body>"
                    self.wfile.write(output.encode(encoding='utf_8'))

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), Handler)
        print('Web server running on port %s' % port)
        server.serve_forever()
    except KeyboardInterrupt:

        print('^C entered, stopping webserver...')
        server.socket.close()


if __name__ == '__main__':
    main()
