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
import urllib.parse

# Initialize main() function
def main():
    # Check the number of command line arguments 
    if len(sys.argv) < 2:
        print("Usage: redact URL")
        return
    else:
        # Create a connection to the server of FOAAS
        connection = http.client.HTTPSConnection('foaas.com')

        # Create the request headers
        headers = {'Accept': 'application/json'}

        # Send a request to over the connection
        connection.request('GET',sys.argv[1], None, headers)

        # Get and read the response
        response = connection.getresponse()
        message = json.loads(response.read())

        # Close a connection
        connection.close()

        # Create a connection to the server of PurgoMalum
        connection2 = http.client.HTTPSConnection('www.purgomalum.com')

        # Set up the message field to send to PurgoMalum's endpoint
        temp = '/service/json?text='+message['message']

        # Encode the message for inclusion in a URL
        url = urllib.parse.quote(temp, safe='?=/')

        # Send a request to over the connection
        connection2.request('GET', url)

        # Get and read the resposnse
        response2 = connection2.getresponse()
        redactedMessage = json.loads(response2.read())

        # Close a connection
        connection2.close()

        # Update the message with the redacted content
        message['message'] = redactedMessage['result']

        # Convert JSON Object into the string with the indented message
        message = json.dumps(message, indent = 4)

        # Show the message on the screen
        print(message)

if __name__ == "__main__":
    main()