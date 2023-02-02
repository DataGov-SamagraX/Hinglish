from flask import Flask, jsonify, request
from utils import final_transliteration,flair_prediction

# creating a Flask app
app = Flask(__name__)

# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods = ['GET'])
def home():
    data = {
        "/" : "GET available endpoints",
        "/translate" : "POST send sentance for translation and transliteration",
        "/sentiment" : "POST sentiment score of sentance (english)" 
    } 
    return jsonify(data)

@app.route('/translate', methods = ['POST'])
def translate():
    recived_data = request.json
    if "sent" not in recived_data:
        return jsonify({"message":"Must contain key sent"})
    sent = recived_data['sent']
    data = final_transliteration(sent)
    return jsonify(data)

@app.route('/sentiment', methods = ['POST'])
def sentiment():
    recived_data = request.json
    if "sent" not in recived_data:
        return jsonify({"message":"Must contain key sent"})
    sent = recived_data['sent']
    data = flair_prediction(sent)
    return jsonify(data)




# driver function
if __name__ == '__main__':

	app.run(debug = True)
