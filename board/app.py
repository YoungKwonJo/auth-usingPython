#sys.setdefaultencoding('utf-8')

from flask import Flask
from flask_cors import CORS
from flask_restplus import Api, Resource, fields

#app = Flask(__name__)
app = Flask(__name__, static_folder='./static')#, template_folder='./static')
### http://localhost:5000/static/index.html
cors = CORS(app, resources={r"*": {"origins": "*"}})

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization2'
    }
}
api = Api(app, version='1.0', title='My board API',
    description='My board API',
    authorizations=authorizations,
)


from model.test import init_db as init_db_test
init_db_test()

from model.auth import init_db as init_db_auth
init_db_auth()

#from model.board import init_db as init_db_board
#init_db_board()




@app.route("/")
def hello():
    return "Hello World!"

from route.test import test
test(api)

from route.auth import auth
auth(api)

#from route.board import board
#board(api)



if __name__ == "__main__":
    app.run(port=5005)
