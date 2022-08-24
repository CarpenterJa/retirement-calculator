from flask import Flask
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin

from calculations import calculate_retirment

app = Flask(__name__, static_folder='client/build', static_url_path='')
cors = CORS(app)

### route for api call from react app
@app.route('/<int:user_id>')
@cross_origin()
def retirment_calculation(user_id):    
    return calculate_retirment(user_id)

### base route for react app
@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run()