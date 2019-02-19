#sys.setdefaultencoding('utf-8')

from flask import Flask
from flask_cors import CORS

#app = Flask(__name__)
app = Flask(__name__, static_folder='./static')#, template_folder='./static')
### http://localhost:5000/static/index.html

cors = CORS(app, resources={r"*": {"origins": "*"}})

from model.test import init_db as init_db_test
init_db_test()

from model.auth import init_db as init_db_auth
init_db_auth()

from model.board import init_db as init_db_board
init_db_board()




@app.route("/")
def hello():
    return "Hello World!"

from route.test import test
test(app)

from route.auth import auth
auth(app)

from route.board import board
board(app)



if __name__ == "__main__":
    app.run()
