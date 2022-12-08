import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from helpers import *
import pickle

# load df
pipe_df = pd.read_csv("../../data/large_sample.csv", index_col = 0)

# don't include this in final code but made a typo when creating the csv
# already fixed in class
pipe_df.drop('red_first_blodd',inplace=True, axis=1)
pipe_df['red_first_blood'] = np.where(pipe_df['blue_first_blood'] == 0, 1, 0)

# set data and target
y = pipe_df['winning_team']
X = pipe_df.drop('winning_team', axis = 1)

# change target variable
y = y.apply(lambda x: 0 if x == 100 else 1)

# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state = 2)

# pipeline
diff = DiffTransformer()

pipe = Pipeline(
    steps = [('diff', diff), ('scaler', StandardScaler()), ('rf', RandomForestClassifier())]
)

pipe.fit(X_train, y_train)

# get score
pipe.score(X_test, y_test)

# tune params
# tune hyper parameters
params = {
    "rf__max_depth": [3,5,7,10],
    "rf__min_samples_split": [2,3,4],
    "rf__min_samples_leaf": [3,5,7],
    "rf__min_weight_fraction_leaf": [0, 0.1]
}
grid = GridSearchCV(pipe, params)
grid.fit(X_train, y_train)

# get best scores
print(grid.best_params_)
print(grid.best_estimator_)
print(grid.best_score_)

grid.score(X_test, y_test)

# pickle
filename = '../../data/trained_model.p'
pickle.dump(grid, open(filename, 'wb'))