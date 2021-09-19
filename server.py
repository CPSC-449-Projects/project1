'''
Members: 1. Vinh Tran (Email: kimvinh@csu.fullerton.edu)
         2. Quang Nguyen (Email: quangdnguyen2211@csu.fullerton.edu)

CPSC 449 - 02

Professor: Kenytt Avery

Project 1: HTTP Clients and Servers
'''

import sys
import json
import http.client
import http.server
import socketserver
import urllib.parse

PORT = 8080;

# Create a subclass of 'http.server.BaseHTTPRequestHandler'
class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(400)
            self.end_headers()
            return
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

        # Create a connection to the server of FOAAS
        connection = http.client.HTTPSConnection('foaas.com')

        # Create the request headers
        headers = { 'Accept': 'application/json' }

        # Send a request to over the connection
        connection.request('GET', self.path, None, headers)

        # Get and read the response
        response = connection.getresponse()
        message = json.loads(response.read())

        # Close a connection
        connection.close()

        # Create a connection to the server of PurgoMalum
        connection2 = http.client.HTTPSConnection('www.purgomalum.com')

        # Set up the message field to send to PurgoMalum's endpoint
        temp = '/service/json?text=' + message['message']

        # Encode the message for inclusion in a URL
        url = urllib.parse.quote(temp, safe='?=/’')

        # Send a request to over the connection
        connection2.request('GET', url)

        # Get and read the resposnse
        response2 = connection2.getresponse()
        redactedMessage = json.loads(response2.read())

        # Close a connection
        connection2.close()

        # Update the message with the redacted content
        message['message'] = redactedMessage['result']

        # Convert the content of 'message' into JSON Object
        message = json.loads(json.dumps(message))

        # Create the HTML Response based on the content of 'message'
        htmlResponse = (
            f"<!DOCTYPE html>"
            f"<html>"
            f"<head>"
            f"	<title>FOAAS - {message['message']} - {message['subtitle']}</title>"
            f"""	<meta charset="utf-8">"""
            f""" <meta property="og:title" content="{message['message']} - {message['subtitle']}">"""
            f""" <meta property="og:description" content="{message['message']} - {message['subtitle']}">"""
            f""" <meta name="twitter:card" content="summary" />"""
            f""" <meta name="twitter:site" content="@foaas" />"""
            f""" <meta name="twitter:title" content="FOAAS: Fuck Off As A Service" />"""
            f""" <meta name="twitter:description" content="{message['message']} - {message['subtitle']}" />"""
            f""" <meta name="viewport" content="width=device-width, initial-scale=1">"""
            f"""	<link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css" rel="stylesheet">"""
            f"</head>"
            f"""<body style="margin-top:40px;">"""
            f"""	<div class="container">"""
            f"""		<div id="view-10">"""
            f"""			<div class="hero-unit">"""
            f"				<h1>{message['message']}</h1>"
            f"				<p><em>{message['subtitle']}</em></p>"
            f"			</div>"
            f"		</div>"
            f"""	<p style="text-align: center"><a href="https://foaas.com">foaas.com</a></p>"""
            f"	</div>"
            f"</body>"
            f"</html>"
            )

        # Show the message on the client's side
        self.wfile.write(htmlResponse.encode())

# Create a TCP Connection
with socketserver.TCPServer(("", PORT), HTTPRequestHandler) as httpd:
    print("[SERVER] - Serving at port", PORT)
    print("[SERVER] - Waiting for a client's request!\n")
    httpd.serve_forever()