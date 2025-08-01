from flask import Flask, request, send_file
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(__name__)

# Configure IBM Watson TTS
authenticator = IAMAuthenticator("YOUR_IBM_WATSON_API_KEY")
tts = TextToSpeechV1(authenticator=authenticator)
tts.set_service_url("YOUR_IBM_WATSON_SERVICE_URL")

@app.route("/api/generate-tts", methods=["POST"])
def generate_tts():
    data = request.json
    text = data["text"]
    tone = data["tone"]
    
    # Map tones to IBM Watson voices
    voices = {
        "neutral": "en-US_AllisonV3Voice",
        "suspenseful": "en-US_MichaelV3Voice",
        "inspiring": "en-US_EmilyV3Voice"
    }
    
    response = tts.synthesize(
        text,
        voice=voices[tone],
        accept="audio/mp3"
    ).get_result()
    
    return send_file(response.content, mimetype="audio/mp3")

if __name__ == "__main__":
    app.run()
