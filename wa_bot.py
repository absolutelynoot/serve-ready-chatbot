from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import model
 
app = Flask(__name__)
 
@app.route("/")
def wa_hello():
    return "Hello, Serve Ready Whatsapp Bot is Running!"
 
@app.route("/wasms", methods=['POST'])
def wa_sms_reply():
    
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    
    msg = request.form.get('Body').lower() # Reading the message from the whatsapp
 
    print("msg-->",msg)
    resp = MessagingResponse()
    reply=resp.message()

    # Create reply
    response = model.getResponse(msg)
    reply.body(response['answer'])
 
    return str(resp)
 
if __name__ == "__main__":	
    app.run(host="0.0.0.0", debug=True)