import sys
import json
import http.client
import http.server
import socketserver
import urllib.parse

PORT = 8080;

def main():
    if (len(sys.argv) < 2):
        print("Usage: redact URL")
        sys.exit()

if __name__ == '__main__':
    main()

# Create a subclass of 'http.server.BaseHTTPRequestHandler'
class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Create a connection to the server of FOAAS
        connection = http.client.HTTPSConnection('foaas.com')

        # Create the request headers
        headers = { 'Accept': 'application/json' }

        # Send a request to over the connection
        connection.request('GET', sys.argv[1], None, headers)

        # Get and read the response
        response = connection.getresponse()
        message = json.loads(response.read())

        # Create a connection to the server of PurgoMalum
        connection2 = http.client.HTTPSConnection('www.purgomalum.com')

        # Send the message field to PurgoMalum's endpoint
        temp = '/service/json?text=' + message['message']

        # Encode the message for inclusion in a URL
        url = urllib.parse.quote(temp, safe='?=/')

        # Send a request to over the connection
        connection2.request('GET', url)

        # Get and read the resposnse
        response2 = connection2.getresponse()
        redactMessage = json.loads(response2.read())

        # Update the message with the redacted content
        message['message'] = redactMessage['result']

        # Convert the content of 'message' into JSON Object
        message = json.loads(json.dumps(message))

        # Convert the strings of 'message' into HTML Response
        htmlResponse = (
            f"<h1>{message['message']}</h1>"
            f"<body>{message['subtitle']}</body>"
            )

        self.wfile.write(htmlResponse.encode())

# Create a TCP Connection
with socketserver.TCPServer(("", PORT), HTTPRequestHandler) as httpd:
    print("[SERVER] Serving at port", PORT)
    print("[SERVER] Waiting for a client's request!")
    httpd.serve_forever()
