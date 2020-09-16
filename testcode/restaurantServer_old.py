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
            elif self.path.endswith('/restaurants/new'):

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = '<html><body>'
                output += \
                    '''<form method = 'POST' enctype='multipart/form-data' action='/restaurants/create'>Name of Restaurant<input name = "message" type = "text"><input type = "submit" value="Submit"></form>'''

                output += '</body></html>'

                self.wfile.write(output.encode(encoding='utf_8'))

                return
            elif self.path.endswith('/edit'):

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurant_id = self.path.split('/')[2]
                restaurant = \
                    session.query(Restaurant).filter(Restaurant.id
                        == restaurant_id).one()

                output = '<html><body>'
                output += '<h2>%s</h2>' % restaurant.name
                output += \
                    "<form method = 'POST' enctype='multipart/form-data' action='/restaurant/%s/updated'><input name = 'name' type = 'text' placeholder = '%s'><input type = 'submit' value = 'Rename'></form>" \
                    % (restaurant.id, restaurant.name)
                output += '</body></html>'

                self.wfile.write(output.encode(encoding='utf_8'))
            elif self.path.endswith('/delete'):

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurant_id = self.path.split('/')[2]
                restaurant = \
                    session.query(Restaurant).filter(Restaurant.id
                        == restaurant_id).one()

                # session.delete(restaurant)
                # session.commit()

                output = '<html><body>'
                output += \
                    '<h1>Are you sure you want to delete %s?</h1>' \
                    % restaurant.name
                output += \
                    "<form method = 'POST' enctype = 'multipart/form-data' action = 'restaurants/%s/delete'><input type = 'submit' value = 'Delete'></form>" \
                    % restaurant.id
                output += '</head></body>'

                self.wfile.write(output.encode(encoding='utf_8'))
        except IOError:

            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            (ctype, pdict) = \
                cgi.parse_header(self.headers.getheader('content-type'))

            if ctype == 'multipart/form-data':

                if self.path.endswith('restaurants/create'):

                    fields = cgi.parse_multipart(self.rfile, pdict)

                    messagecontent = fields.get('message')

                    newRestaurant = Restaurant(name='%s'
                            % messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    output = '<html><body>'
                    output += \
                        'Restaurant has been added to the database! Please go back to '
                    output += \
                        '<a href = /restaurants>Restaurants List</a>'
                    output += '</html></body>'

                    self.wfile.write(output.encode(encoding='utf_8'))

                elif self.path.endswith('updated'):

                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')
                    restaurant_id = self.path.split('/')[2]

                    restaurant = \
                        session.query(Restaurant).filter(Restaurant.id
                            == restaurant_id).one()

                    restaurant.name = messagecontent[0]
                    session.add(restaurant)
                    session.commit()

                    output = '<html><head>'
                    output += \
                        '<meta http-equiv = "refresh" content = "0;url=/restaurants">'
                    output += '</head></html>'

                    self.wfile.write(output.encode(encoding='utf_8'))
                elif self.path.endswith('delete'):

                    restaurant_id = self.path.split('/')[2]

                    restaurant = \
                        session.query(Restaurant).filter(Restaurant.id
                            == restaurant_id).one()

                    session.delete(restaurant)
                    session.commit()if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Location', '/restaurant')
                # self.send_header('Content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Create new restaurant"
                output += '<h2> Enter the restaurant name </h2>'
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/new'><input name='restaurantName' type='text'><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output.encode(encoding='utf_8'))
                #print(output)
                return

                    output = '<html><head>'
                    output += \
                        "<meta http-equiv = 'refresh' content=0;url='/restaurants'> "
                    output += '</head></html>'

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
