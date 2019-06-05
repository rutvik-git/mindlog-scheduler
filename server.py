from os import environ
from flask import Flask

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Book, MoodData, UserData

@app.route("/")
def hello():
    return "Hello World!"
    
app.run()
