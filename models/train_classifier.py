from sqlalchemy import create_engine
import sys
import pandas as pd
import re
import nltk
import pickle
from nltk.corpus import stopwords
nltk.download(['punkt', 'stopwords', 'wordnet'])
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

def load_data(database_filepath):
    #input is a string of database path, loads data from the path and divides the data to input and output variables for a machine learning pipeline
    engine = create_engine('sqlite:///{}'.format(database_filepath))
    df = pd.read_sql_table('cleaned_message_data', engine)
    X = df['message']
    Y = df.drop(columns=['id', 'original', 'genre', 'message'], axis=1)
    return X, Y


def tokenize(text):
    #input is a text that gets cleaned, tokenized and lemmatized
    text = text.lower()
    text = re.sub(r"[^a-z1-9]", " ", text)
    words = nltk.word_tokenize(text)
    words = [w for w in words if w not in stopwords.words("english")]
    lemmed = [WordNetLemmatizer().lemmatize(w) for w in words]
    
    return lemmed


def build_model():
    #builds a pipeline and a gridsearch model
    pipeline = Pipeline([
                ('vect', CountVectorizer(tokenizer=tokenize)),
                ('tfidf', TfidfTransformer()),
                ('classifier', MultiOutputClassifier(RandomForestClassifier()))
                ])
    parameters = {
        'classifier__estimator__n_estimators': [50, 100]
    }

    cv = GridSearchCV(pipeline, param_grid=parameters) 
    return cv


def evaluate_model(model, X_test, Y_test):
    #inputs a model and test data, predicts according to model and prints out evaluation for each category
    preds = model.predict(X_test)
    preds_df = pd.DataFrame(data=preds, columns=Y_test.columns)
    for col in Y_test:
        print(classification_report(Y_test[col], preds_df[col], labels=[0, 1]))

def save_model(model, model_filepath):
    #saves the model
    with open(model_filepath, 'wb') as f:
        pickle.dump(model, f)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()