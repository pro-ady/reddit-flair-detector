# Reddit Flair Detector

---
The link to the web app. Currently Live !!
[Reddit Flair Detector](https://reddit-flair-detector-aditya.herokuapp.com/)

---

### REPRODUCE THIS APP LOCALLY
On Ubuntu
1. Clone this repository and unzip
2. ``$ cd reddit-flair-detector && pip install -r requirements.txt``
3. ``$ python3 app.py``
4. The application will start running on the localhost at the port mentioned in the terminal
5. To deploy to Heroku, simply follow [these steps](https://devcenter.heroku.com/articles/getting-started-with-python)
---

### INDEX
1. About the project
2. Data Acquisition
3. Data Visualisation, Preprocessing and Cleaning
4. Data Modelling and Flair Detection
5. Creation of Web Application and Deployment
---

### 1. ABOUT THE PROJECT
The aim of the project was to detect the flair of a post belonging to the r/india subreddit, given the URL of the post(s). The project is built on Python3 and mainly uses the following dependencies:
- Pandas (for handling of dataframes)
- Numpy 
- scikit-learn (for the various machine learning models)
- nltk (for NLP)
- Flask (for Web App Development)
---

### 2. DATA ACQUISITION 
Data acquisition was achieved using the [praw](https://praw.readthedocs.io/en/latest/) tool. Firstly we identified the different flairs available in the subreddit which were as follows:
- "Sports", 
- "Politics",
- "AskIndia", 
- "Business/Finance", 
- "Food",
- "Science/Technology", 
- "Non-Political", 
- "Photography", 
- "Policy/Economy", 
- "Scheduled", 
- "[R]eddiquette"

For each of the flairs, an attempt was made to acquire as much quantity of posts, however, due to limitations within the praw tool, only a limited quantity (~100 posts per flair) were acquired. We obtained various information for each of the posts including body, comments, title, URL, actual_flair, permalink (which is a shortened form of the url but has a standard format unlike the URL which may point to external pages)

An alternative to the data acquisition was found. It made use of the Google Cloud Platform and on sending a query to the same, Reddit posts (~15000 posts) were made available in a short period of time. However, on further inspection, data was found to be unusable since it was outdated and prediction of our model could have gotten inaccurate. Further comments associated with each posts still had to be acquired using the praw tool.

Nevertheless, if one wishes to acquire that data, the query used was as follows

    'SELECT * except (domain, subreddit, author_flair_text,    'from_kind, saved, hide_score, archived, from_id, name, quarantine, distinguished,thumbnail, is_self, retrieved_on, gilded, subreddit_id)' 
    'FROM `fh-bigquery.reddit_posts.201*`'
    'WHERE subreddit = "india" and link_flair_text in ("Sports", "Politics", "AskIndia", "Business/Finance", "Food", "Science/Technology", "Non-Political", "Photography", "Policy/Economy", "Scheduled", "[R]eddiquette")'
    'LIMIT 15000' 

The data acquired was saved as it is to [this file](https://github.com/pro-ady/reddit-flair-detector/blob/master/data/reddit_data_raw.csv).

---
### 3. DATA VISUALIZATION
Data acquired in the raw form can no case be used as it is. Hence we had to format or clean it to move on to the next step. However in this project, we couldn't clean the data unless we knew exactly how the data was present and what could be done to "clean" it. We used Data Visualisation for this.

- First step involved seeing how many posts of each flair do we have and how evenly was the quantity distributed. We saw that every flair, with the exception of Reddiquette had ~100 posts each. At this point itself, we could have said that the prediction accuracy for Reddiquette would be low since we don't have enough posts. But we shall deal with that later.

- Next we needed to see, how much of the data was empty (NaN) or non-empty, because sending in NaN into the models will cause unnecessary errors. Hence whenever we needed to consider NaN fields, we replaced them with a blank space (" ")

- Next we visualize what words needed to be removed and draw a frequency plot for the words in for each of the field and each of the flair. For this we made use of a simple Seaborn barplot which plotted a word against the number of times it occured in the text.
Eg. In the following image we see that for a given field, the distribution of words along with the frequency. We see that words like https, com, like, just, etc. are not something which are unique to the Politics flair unlike some of the more prominent ones. Hence, using this method we can decide which of the words to include and which to add to the stopwords.


![Fig. 1](https://i.ibb.co/41g22H1/index.png)

We repeat this visualization process for all the combination of parameters and flairs. Hence obtaining, an exhaustive list of words that need to be excluded before we create a model.

Next, we make use of the nltk package to perform lemmatization of the text fields. Next, we combine different on which our prediction could depend on.

We shall export this preprocessed and cleaned data into [this file](https://github.com/pro-ady/reddit-flair-detector/blob/master/data/reddit_data_preprocessed.csv)

---
### 4. DATA MODELLING
Our first step was to choose the combination of labels on which we intended to train our models. Since we didn't have the knowledge of which parameter had the highest influence on the flair, we considered the following combinations:
- only body
- only comments
- only title
- only URL
- body + comments
- all parameter

We used Count Vectorizer and TFIDF Vectorizer individually. 

We used 3 Models to test our data on:
- Logistic Regression (both 'l1' penalty and 'l2' penalty)
- Support Vector Machine (Classifier)
- Random Forest

The accuracy for each of the possible combinations was calculated and stored in a table as follows 

|Label Considered    |Vectorizer      |Model|Train Accuracy|Test Accuracy|
|---------------|----------------|-----|--------------|-------------|
|body           |Count Vectorizer|LR   |49.2          |23.2         |
|body           |Count Vectorizer|SVC  |39.07         |23.6         |
|body           |Count Vectorizer|RF   |62.53         |43.6         |
|body           |TFIDF Vectorizer|LR   |52.0          |32.4         |
|body           |TFIDF Vectorizer|SVC  |15.47         |16.8         |
|body           |TFIDF Vectorizer|RF   |60.8          |32.8         |
|comments       |Count Vectorizer|LR   |52.0          |14.8         |
|comments       |Count Vectorizer|SVC  |20.4          |12.4         |
|comments       |Count Vectorizer|RF   |62.0          |18.0         |
|comments       |TFIDF Vectorizer|LR   |68.27         |16.4         |
|comments       |TFIDF Vectorizer|SVC  |11.87         |10.8         |
|comments       |TFIDF Vectorizer|RF   |52.4          |16.0         |
|title          |Count Vectorizer|LR   |83.47         |69.6         |
|title          |Count Vectorizer|SVC  |46.27         |40.8         |
|title          |Count Vectorizer|RF   |81.07         |70.4         |
|title          |TFIDF Vectorizer|LR   |91.47         |72.4         |
|title          |TFIDF Vectorizer|SVC  |13.6          |12.4         |
|title          |TFIDF Vectorizer|RF   |76.27         |71.2         |
|URL            |Count Vectorizer|LR   |65.87         |50.8         |
|URL            |Count Vectorizer|SVC  |44.4          |38.8         |
|URL            |Count Vectorizer|RF   |69.73         |55.6         |
|URL            |TFIDF Vectorizer|LR   |88.13         |53.6         |
|URL            |TFIDF Vectorizer|SVC  |12.8          |12.4         |
|URL            |TFIDF Vectorizer|RF   |61.47         |51.6         |
|body + comments|Count Vectorizer|LR   |55.33         |25.2         |
|body + comments|Count Vectorizer|SVC  |47.07         |24.0         |
|body + comments|Count Vectorizer|RF   |80.27         |45.6         |
|body + comments|TFIDF Vectorizer|LR   |75.73         |38.4         |
|body + comments|TFIDF Vectorizer|SVC  |14.13         |13.6         |
|body + comments|TFIDF Vectorizer|RF   |77.33         |34.4         |
|All Params     |Count Vectorizer|LR   |68.53         |42.0         |
|All Params     |Count Vectorizer|SVC  |77.33         |46.8         |
|**All Params**     |**Count Vectorizer**|**RF**   |**95.73**         |**82.8**         |
|All Params     |TFIDF Vectorizer|LR   |90.4          |70.0         |
|All Params     |TFIDF Vectorizer|SVC  |13.47         |12.8         |
|All Params     |TFIDF Vectorizer|RF   |92.0          |72.8         |
LR = Logistic Regression
SVC = Support Vector Classifier
RF = Random Forest

We concluded that the model and combination marked in bold had the highest accuracy of all the models, and it would be wise to consider it for our final model due to its considerable **test accuracy**. (training accuracy is high but that doesn't imply that the model is ideal)

Further the confusion matrix for that model was as follows

![](https://i.ibb.co/PhPLZCn/Screenshot-from-2020-04-16-22-41-36.png)

We observe that the correctly predict flair for the Reddiquette flairs is extremely low, and hence we say that **our model is unfit to predict posts of that flair within certain confidence**.

In order to slightly improve the accuracy, we run the same model without considering the posts of the Reddiquette flair. Hence, we decide to export this model using the [Pickle](https://docs.python.org/3/library/pickle.html) tool.

---
### 5. CREATION OF WEB APPLICATION AND DEPLOYMENT
We create a web application with the help of flask package. The web application works in the following way:
1. Inputs the URL of the Reddit post
2. Passes the URL to a function which retrieves the information about the post
3. Cleans the information received and combines the fields
4. Imports the saved model and predicts the flair according to the current input
5. Outputs the predicted flair

The app was then deployed on to Heroku (link given at the top)

ADDITIONAL FEATURE:
A route ```/automated_testing``` to which you could send a text file (.txt) as a POST request, with the text file containing URL of individual Reddit posts in each new line, and the output will be a JSON file which has an object of JS Objects containing the URL as well as the predicted flairs of the Reddit posts. 

---  
Downsides of the model:
- It doesn't classify posts belonging to the Reddiquette flair
- It doesn't work well with posts which have a low amount of content or in which comments is not present at all
- Certain posts of the Politics flair may get classified under the Politics category since both have a major resemblance in the word distribution 

Upsides of the model:
- Works well with posts having sufficient content
- Has fairly high accuracy (i.e. 82%)


A few suggestions:
- Add a file nltk.txt to the root directory, since Heroku isn't able to download the corpus for nltk without it (the contents of the nltk file are given above)
- Run the logistic regression with a 'l1' penalty, since it gave higher accuracy than 'l2'
- Run the project inside a virtual environment
