from flask import Flask
from flask_cors import CORS
from getFiles import upload
app=Flask(__name__)
CORS(app)
upload(app)
if __name__=="__main__":
    print("The program has started.")
    app.run(debug=True)