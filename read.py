import sys
import json
import http.client
import urllib.parse

connection = http.client.HTTPSConnection('foaas.com')
headers={'Accept': 'application/json'}
connection.request('GET',sys.argv[1], None, headers)
response = connection.getresponse()
message = json.loads(response.read())

connection2 = http.client.HTTPSConnection('www.purgomalum.com')
temp = '/service/json?text='+message['message']
url = urllib.parse.quote(temp, safe='?=/')
connection2.request('GET', url)
response2 = connection2.getresponse()
redactMessage = json.loads(response2.read())

message['message'] = redactMessage['result']
result = json.dumps(message)
print(result)
