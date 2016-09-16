import os
from sklearn.datasets import load_files
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.svm import LinearSVC
from sklearn import metrics

dataset_dir_name = os.getcwd() + '/txt_sentoken'

# load data,and split into training/test set
movie_reviews = load_files(dataset_dir_name)
print movie_reviews.target

# split
doc_terms_train, doc_terms_test, doc_class_train, doc_class_test = train_test_split(
    movie_reviews.data, movie_reviews.target, test_size=0.2, random_state=None)

# build a vectorizer/classifier pipeline
pipeline = Pipeline([
    ('vect', TfidfVectorizer(min_df=3, max_df=0.95)),
    ('clf', LinearSVC(C=1000)),
])

# grid search
parameters = {
    'vect__ngram_range': [(1, 1), (1, 2)],
}
grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1)
grid_search.fit(doc_terms_train, doc_class_train)
# print grid_search.grid_scores_

# y_predicted
y_predicted = grid_search.predict(doc_terms_test)

# report
print metrics.classification_report(
    doc_class_test, y_predicted, target_names=movie_reviews.target_names)

# confusion matrix
# confusion_matrix = metrics.confusion_matrix(doc_class_test, y_predicted)
# print confusion_matrix
