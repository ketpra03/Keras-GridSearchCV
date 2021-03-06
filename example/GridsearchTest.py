import sys
sys.path.append('../') #Included to do the import of kerasGridSearchCV
import numpy
from gridsearch.kerasGridSearch import kerasGridSearchCV  # Import Gridsearch

# The example code comes mainly from
# https://machinelearningmastery.com/grid-search-hyperparameters-deep-learning-models-python-keras/
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
# Function to create model, required for KerasClassifier

# We need the keras backend for cleaning the GPU after each train/test step in the Cross Validation
from keras import backend as K
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR) #This is useful to avoid the info log of tensorflow
# The next 4 lines are for avoiding tensorflow to allocate all the GPU memory
config = tf.ConfigProto()
config.gpu_options.allow_growth=True
sess = tf.Session(config=config)
K.set_session(sess)

# Code from Machine learning mastery
def create_model():
	# create model
	model = Sequential()
	model.add(Dense(12, input_dim=8, activation='relu'))
	model.add(Dense(1, activation='sigmoid'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model
# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
# load dataset
dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]
# create model
model = KerasClassifier(build_fn=create_model, verbose=0)
# define the grid search parameters
batch_size = [10, 20, 40, 60, 80, 100]
epochs = [10, 50, 100]
param_grid = dict(batch_size=batch_size, epochs=epochs)
# Instead of GridsearchCV, kerasGridSearchCV which implements a minor change in the fit function.
# There is a problem with tensorflow when using n_jobs > 1, where the code hangs without doing any grid search
grid = kerasGridSearchCV(estimator=model, param_grid=param_grid, n_jobs=1, cv=3,verbose=1)
grid_result = grid.fit(X, Y, session = K) #We pass the keras backend (K) in the session parameter of the fit function
# Code from machine learning mastery
# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
	print("%f (%f) with: %r" % (mean, stdev, param))