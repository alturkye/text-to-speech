import zmq
import json

from playsound import playsound

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")
#list = [] put this input into text to get the error status
message = "This is a text to make sure the text to speech microservice works!"

data = {
    "text": message,
    "voice": "male"
}

print("test.py attempting to connect to server...")

print(f"Sending a request...")

socket.send_json(data)

received = socket.recv_json()

print(f"service.py was a {received['status']}")
if received['status'] == "error":
    print("Check to make sure your input is a piece of text")
else:
    audio_path = received["file_path"]

    playsound(audio_path)

