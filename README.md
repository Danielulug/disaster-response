# Disaster Response Pipeline Project
A project that aims to handle messages received in time of disaster and label an appropriate category for the message. This would help respondents to find people in help faster and even arrange messages for the right departments in times of disaster. 

process_data.py is functioning as the etl pipeline with three arguments: message data path, category data path and desired database name. This is where the data is processed, cleaned and put in to a sql database.
process_data.py is functioning as the machine learning pipeline with two arguments: sql database path that has the data and and desired model output name. This script creates machine learning solution for the provided database.
run.py is the script that is creating the web app. Takes no arguments and creates a local web app with port 3001.


### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/
