from flask import Flask, session
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.secret_key = "SECRET_KEY"
bcrypt = Bcrypt(app)
DB = "recipe_schema"