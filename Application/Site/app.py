from flask import  Flask, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def index():
	#author = "Michael"
	#name = "Sir"
	#return render_template('index.html', author=author, name=name)
	return render_template('index.html')


@app.route('/data')
def names():
	data={"names": ['John', 'Jacob', 'Julie', 'Jennifer']}
	return jsonify(data)


if __name__ == '__main__':
	app.run()

