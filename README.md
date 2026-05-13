# Text-to-Speech (TTS) Microservice

## Description
This service converts text strings into audio files using a local TTS engine.
It is designed to be called asynchronously via ZeroMQ

## Communication Contract 

### How to REQUEST data
Requests should be made using a ZeroMQ REQ socket
* PORT: 5556
* FORMAT: JSON object 

* Example call * 
import zmq 
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

socket.send_json({"text": "Hello, this is a test.", "voice": "male"})

### How to RECEIVE data 
Once the microservice process the request, it will send a response back through
	the same ZeroMQ pipe 
The service will return a JSON object with an URL path to the audio file or file path   

* Example call * 
response = socket.recv_json()

if response["status"] == "success":
	print(f"success, audio saved at: {response['file_path']}")
else:
	print(f"Error: {response['message']}")
