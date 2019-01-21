#sys.setdefaultencoding('utf-8')

from flask import Flask
from flask_cors import CORS

#app = Flask(__name__)
app = Flask(__name__, static_folder='./static/', template_folder='./static')
### http://localhost:5000/static/index.html

cors = CORS(app, resources={r"*": {"origins": "*"}})

from model.test import init_db as init_db_test
init_db_test()



@app.route("/")
def hello():
    return "Hello World!"

from route.test import test
test(app)



if __name__ == "__main__":
    app.run()
