# Members: Vinh Tran (Email: kimvinh@csu.fullerton.edu)
	   Quang Nguyen (Email: quangdnguyen2211@csu.fullerton.edu)

# CPSC 449 - 02

# Professor: Kenytt Avery

# Project 1: HTTP Clients and Servers

----------------------------------------------------------------------------------------------------

### SUMMARY ###

- The programs were designed to connect to FOAAS's server to retrieve the appropriate content from the requested URL. 
Then, that content will be passed through the PurgoMalum service to render the redacted message that is suited to the professional language. 
The task works either by a command-line utility or by a client-server model.

----------------------------------------------------------------------------------------------------

### DOCUMENTATION ###

- For program #1, the URL path from the command line will be taken by using sys.argv and used to make a HTTP connection with the header Accept: application/json. 
The response will be deserialized to a string and encoded to be the path URL to Purgo Malum server to get the redacted message.

- For program #2, the program will first connect to a local host server then it will do what program #1 does.
After that, the redacted message will be displayed on the web browser with the template of FOAAS.

----------------------------------------------------------------------------------------------------

### "CPSC-449-Project1.tar.gz" Contents ###

1. README.txt		// This file

2. redact.py		// Containing the source code that executives the program #1

3. server.py		// Containing the source code that executives the program #2

4. sample_output.png	// The sample output of the program #2

----------------------------------------------------------------------------------------------------

### Run The Program ###

- For more information about options for the requested URL, please visit a website: http://www.foaas.com

# Program #1 #

- To run the program, command: $ python3 redact.py path-to-foaas

For example: $ python3 redacted.py /because/Vinny

- Expected Output:

{
    "message": "Why? Because **** you, that's why.",
    "subtitle": "- Vinny"
}

# Program #2 #

1. To run the program, command: $ python3 server.py

2. The server is open to wait for the client's request with the following messages:

[SERVER] - Serving at port 8080
[SERVER] - Waiting for a client's request!

3. Open the browser and enter: http://localhost:8080/[URL]

For example: http://localhost:8080/because/Vinny

4. Then, the server will response the content based on the requested URL on the browser.

5. Please open "sample_output.png" to see the output.

*Note: The server will keep opening and waiting for the client's request until the program is closed.
