import zmq
import pyttsx3
import json
import os

# initalize the TTS engine
engine = pyttsx3.init()

# set up ZeroMQ
context = zmq.Context()
socket = context.socket(zmq.REP) # rep = reply, the listener
socket.bind("tcp://*:5556")

print("TTS service is running on port 5556...")

while True:
    message = socket.recv_json()
    text_to_speak = message.get("text", "")
    voice_type = message.get("voice", "female")

    print(f"Received request: {text_to_speak}")

    if text_to_speak:
        # generate the audio file
        if not os.path.exists('audio'):
            os.makedirs('audio')

        file_path = "./audio/output.wav"
        engine.save_to_file(text_to_speak, file_path)
        engine.runAndWait()

        # send back success response
        socket.send_json({
            "status": "success",
            "file_path": file_path
        })
    else:
        socket.send_json({"status": "error", "message": "No text provided"})
