from flask import Flask, render_template,request, jsonify, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pickle
import script
import os
import json

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")

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
def automated_testing():
	print(request.files)
	attachment = request.files['upload_file']
	urls = attachment.read()
	if urls == "":
		if 'url' not in request.args:
			return render_template('error.html', error_message="No input provided")

		else:
			URL = request.args['url']
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

				final_result = {
					URL: predicted_flair
				}

				return jsonify(final_result)

	elif 'upload_file' in request.files:
		dirname = os.path.dirname(__file__)
		filename = str(dirname) + "/models/CVRF_allParams.sav"
		print('\n\n\n\n')
		print(dirname, " ",filename)
		print('\n\n\n\n')
		loaded_model = pickle.load(open(filename, 'rb'))
		
		urls = urls.decode("utf-8")

		print("\n\n\n\n")
		print(urls)
		print("\n\n\n\n")

		urls_list = str(urls).split('\n')

		print(urls_list)

		myObj = {}

		for url in urls_list:
			check_error, error_message = script.checkRedditURL(url)

			if check_error == False:
				element = {
					str(url): str("Link error " + error_message)
				}
				myObj.update(element)

			else:
				X_test,actual_flair = script.getData_usingPraw(url)
				predicted_flair = loaded_model.predict([X_test])[0]

				element = {
					str(url): predicted_flair
				}

				myObj.update(element)
			
		return json.dumps(myObj)


if __name__ == "__main__":
	app.run(threaded=True, port=5000, debug=True)


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