#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import math
from scipy.misc import comb
def enseble_error(n_classifier, error):
	k_start = int(math.ceil(n_classifier / 2))
	probs = [comb(n_classifier, k) * error**k * (1-error) ** (n_classifier-k) for k in range(k_start, n_classifier+1)]
	return sum(probs)

from sklearn.base import BaseEstimator
from sklearn.base import ClassifierMixin
from sklearn.preprocessing import LabelEncoder
from sklearn.externals import six
from sklearn.base import clone
from sklearn.pipeline import _name_estimators
import operator
class MajorityVoteClassifier(BaseEstimator, ClassifierMixin):
	'''A majority vote ensemble classifier
	Parameters
	---------
	classifiers: array-like, shape=[n_classifers]
		Different classifiers for the ensemble
	vote: str,{'classlabel', 'probability'}
		Default: 'classlable'
		If 'classlable' the prediction is based on the argmax of class labels.
		Else if 'probability', the argmax of the sum of probabilities is used
		to predict the class label (recommended for calibrate classifiers).
	weights: array-linke, shape=[n_classifiers]
		Optinal, default: None
		If a list of int or float values are provided, the classifiers are weighted
		by importance; Uses uniform weights if weights=None/
	'''
	def __init__(self, classifiers, vote='classlabel', weighths=None):
		self.classifiers = classifiers
		self.named_classifiers = {key: value for key,value in _name_estimators(classifiers)}
		self.vote = vote
		self.weights = weights

	def fit(self, X, y):
		'''Fit classifiers.
		Parameters
		----------
		X: {array-like, sparse matrix},
			shape = [n_samples, n_features]
			Matrix of training samples.
		y: array-like, shape=[n_samples]
			Vector of target class lables.'
		Returns
		-------
		self: object
		'''
		# Use LabeleEncoder to ensure class labels start with 0, which is important for np.argmax
		# call in self.predict
		self.lablenc_ = LabelEncoder()
		self.lablenc_.fit(y)
		self.class_ = self.lablenc_.classes_
		self.classifers_ = []
		for clf in self.classifiers:
			fitted_clf = clone(clf).fit(X, self.lablenc_.transform(y))
			self.classifiers_.append(fitted_clf)
		return self

	def predict(self, X):
		'''Predict class labels for X.
		Parameters
		----------
		X: {array-like, sparse matrix},
			Shape = [n_samples, n_features]
			Matrix of training samples.
		Returns
		-------
		maj_vote: array-like, shape=[n_samples]
			Predicted class labels.
		'''
		if self.vote == 'probability':
			maj_vote = np.argmax(self.predict_proba(X), axis=1)
		else: # 'classlabel' vote
			# collect results from clf.predict calls
			predictions = np.asarray([clf.predict(X) for clf in self.classifiers_]).T
			maj_vote = np.apply_along_axis(lambda x: np.argmax(np.bincount(X, weights=self.weights)), axis=1, arr=predictions)
		maj_vote = self.lablenc_.inverse_transform(maj_vote)
		return maj_vote

	def predict_proba(self, X):
		'''Predict class probabiliyies for X.
		Paramters
		---------
		X: {array-linke, sparse matrix},
			shape = [n_samples, n_features]
			Training vectors, where n_samples is the number of samples and n_featrues is the number of features.
		Returns
		-------
		avg_proba: array-linke, 
			shape = [n_samples, n_classes]
			Weighted average probability for each class per sample.
		'''
		probas = np.asarray([clf.predict_proba(X) for clf in self.classifiers_])
		avg_proba = np.average(probas, axis=0, weigths=self.weights)
		return avg_proba

	def get_params(self, deep=True):
		'''Get classifier papameter names for GridSearch.'''
		if not deep:
			return super(MajorityVoteClassifier, self).get_params(deep=False)
		else:
			out = self.named_classifiers.copy()
			for name, step in six.iteritems(self.named_classifiers):
				for key,value in six.iteritems(step.get_params(deep=True)):
					out['%s_%s' % (name,key)] = value
			return out

if __name__ == '__main__':
	print(enseble_error(n_classifier=11, error=0.25))
	error_range = np.arange(0, 1.01, 0.001)
	ens_errors = [enseble_error(n_classifier=11, error=error) for error in error_range]
	fig = plt.figure()
	plt.plot(error_range, ens_errors, label='Ensemble error', linewidth=2)
	plt.plot(error_range, error_range, linestyle='--', label='Base error', linewidth=2)
	plt.xlabel('Base error')
	plt.ylabel('Base/Ensemble error')
	plt.legend(loc='upper left')
	plt.grid(alpha=0.5)
	fig.savefig('ensemble.pdf')

	from sklearn import datasets
	from sklearn.model_selection import train_test_split
	from sklearn.preprocessing import StandardScaler
	from sklearn.preprocessing import LabelEncoder
	iris = datasets.load_iris()
	X, y = iris.data[50:, [1,2]], iris.target[50:]
	le = LabelEncoder()
	y = le.fit_transform(y)

