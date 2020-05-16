#from flask import Flask
#app = Flask(__name__)
#@app.route("/")
#def main():
#    return "SAIBABA"
#if __name__ == "__main__":
#    app.run(host= '0.0.0.0')

#from flask import Flask, render_template
#app = Flask(__name__)
#@app.route("/")
#def main():
#    return render_template('index.html')
#if __name__ == "__main__":
#     app.run(host= '0.0.0.0')
#     app.run()
from flask import Flask, render_template
from flask import send_from_directory
app = Flask(__name__)

@app.route("/")
def main():
   return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
   return render_template('signup.html')


if __name__ == "__main__":
   app.run(host="0.0.0.0")
