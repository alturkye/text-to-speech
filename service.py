import zmq
import pyttsx3
import json
import os

# initalize the TTS engine


# set up ZeroMQ
context = zmq.Context()
socket = context.socket(zmq.REP) # rep = reply, the listener
socket.bind("tcp://*:5556")

print("TTS service is running on port 5556...")

while True:
    message = socket.recv_json()
    text_to_speak = message.get("text", "")
    voice_type = message.get("voice", "female")

    engine = pyttsx3.init() # Moved the engine into the while loop so a new one is intialized for every request. Makes multiple request in a row work 
    voices = engine.getProperty("voices")
    if voice_type == "female":
        engine.setProperty("voice", voices[1].id)  # Switches from male to female depending on what was in the request
    else:
        engine.setProperty("voice", voices[0].id)

    print(f"Received request: {text_to_speak}")
    

    if text_to_speak:
        # generate the audio file
        if not os.path.exists('audio'):
            os.makedirs('audio')

        file_path = "./audio/output.wav"

        engine.save_to_file(text_to_speak, file_path)

        engine.runAndWait()

        engine.stop() # Deletes the engine
        del engine

        # send back success response
        socket.send_json({
            "status": "success",
            "file_path": file_path
        })
    else:
        socket.send_json({"status": "error", "message": "No text provided"})
        engine.stop()
        del engine
