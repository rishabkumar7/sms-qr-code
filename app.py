# Imports
from flask import Flask, request, send_file
from twilio.twiml.messaging_response import MessagingResponse
from PIL import Image
import qrcode
import re

app = Flask(__name__, static_folder='qrcodes')


@app.route("/generate", methods=['POST'])
def generate_qr_code():
    inb_msg = request.form['Body'].lower()
    print(inb_msg)
    url = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', inb_msg)
    url = url[0]
    print(f"Generating QR Code for {url}")
    try:
        resp = MessagingResponse()
        msg = resp.message()
        resp.message('Hello, we are generating your QR Code, please wait...')
        img = qrcode.make(inb_msg)
        urlclean = url.replace("https://", "")
        filename = f"{urlclean}.png"
        img.save("./qrcodes/" + filename)
        msg.media("./qrcodes/" + filename)
        return str(resp), 200
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    app.run(debug=True, port = 5100)