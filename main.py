from flask import Flask, render_template,request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pickle
import script
import os

app = Flask(__name__)


@app.route("/flair", methods=['POST'])
def flair():
	URL = request.form['redditURL']

	check_error, error_message = script.checkRedditURL(URL)

	if check_error == False:
		return render_template('error.html', error_message=error_message)

	else:
		X_test,actual_flair = script.getData_usingPraw(URL)
		dirname = os.path.dirname(__file__)
		filename = str(dirname) + "/models/CVRF_allParams.sav"
		print(dirname, " ",filename)
		loaded_model = pickle.load(open(filename, 'rb'))
		predicted_flair = loaded_model.predict([X_test])[0]

		return render_template('flair.html', predicted_flair=predicted_flair)


@app.route("/automated_testing", methods=['POST'])
def automated_testing_file():
	if 'attachment' not in request.files:
		if 'url' not in request.args:
			return render_template('error.html', error_message="No input provided")

		else:
			URL = request.args['url']
			check_error, error_message = script.checkRedditURL(URL)

			if check_error == False:
				return error_message

			else:
				X_test,actual_flair = script.getData_usingPraw(URL)
				dirname = os.path.dirname(__file__)
				filename = str(dirname) + "/models/CVRF_allParams.sav"
				print(dirname, " ",filename)
				loaded_model = pickle.load(open(filename, 'rb'))
				predicted_flair = loaded_model.predict([X_test])[0]

				final_result = {
					"key": URL,
					"value": predicted_flair
				}

				return jsonify(final_result)

	elif 'attachment' in request.files:
		dirname = os.path.dirname(__file__)
		filename = str(dirname) + "/models/CVRF_allParams.sav"
		print(dirname, " ",filename)
		loaded_model = pickle.load(open(filename, 'rb'))
		attachment = request.files['attachment']

		urls = attachment.read()
		urls = urls.decode("utf-8")

		print("\n\n\n\n")
		print(urls)
		print("\n\n\n\n")

		urls_list = str(urls).split('\n')

		print(urls_list)

		array = []

		for url in urls_list:
			check_error, error_message = script.checkRedditURL(url)

			if check_error == False:
				element = {
					"key": url,
					"value": str("Link error " + error_message)
				}
				array.append(element)

			else:
				X_test,actual_flair = script.getData_usingPraw(url)
				predicted_flair = loaded_model.predict([X_test])[0]

				element = {
					"key": url,
					"value": predicted_flair
				}

				array.append(element)
			
		return jsonify(array[:-1])

@app.route("/")
def home():
	return render_template("home.html")

if __name__ == "__main__":
	app.run(threaded=True, port=5000)


# @app.route("/automated_testing", methods=['POST'])
# def automated_testing():
# 	URL = request.args['url']
# 	check_error, error_message = script.checkRedditURL(URL)

# 	if check_error == False:
# 		return error_message

# 	else:
# 		X_test,actual_flair = script.getData_usingPraw(URL)
# 		dirname = os.path.dirname(__file__)
# 		filename = str(dirname) + "/models/CVRF_allParams.sav"
# 		print(dirname, " ",filename)
# 		loaded_model = pickle.load(open(filename, 'rb'))
# 		predicted_flair = loaded_model.predict([X_test])[0]

# 		final_result = {
# 			"key": URL,
# 			"value": predicted_flair
# 		}

# 		return jsonify(final_result)

	#return "You've reached testing"

	# array = []

	# for i in file_input:
	# 	element = {
	# 		"x":str(i)
	# 	}
	# 	array.append(element)

	# return jsonify(array)