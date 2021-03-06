#!/usr/bin/env python3 -w ignore DataConversionWarning
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.feature_selection import RFECV

from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

def boxplot(column):
    # to do: return a boxplot of each variables
    return 0

def plotHist(column, title, x_label, y_label):
    # to do: plot histogram for each individual variable
    binwidth = [x for x in range(0,20000, 2000)]
    ex = plt.hist(column, bins=binwidth)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    return plt.show()

def plotHistTwo(colA, colB, title="", x_label="", y_label="frequency"):
    # to do: plot a two way histogram for male female for each variable
    binwidth = [x for x in range(0,30000, 1000)]
    # plt.hist(colA, bins=binwidth, alpha=0.5, label = "favNumberMales")
    # plt.hist(colB, bins=binwidth, alpha=0.5, label = "favNumberFemales")
    plt.hist([colA, colB], bins=binwidth, alpha=0.5, label=["tweetCountMales", "tweetCountFemales"])
    plt.legend(loc='upper right')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    return plt.show()

def scatter(col1, col2):
    # to do: plot a scatter plot for variables. E.g. hue vs brightness with
    # male and female colored differently
    return 0

def main():
    #################### SETUP CODE ########################################
    # start time
    startTime = time.time()

    # load the dataset
    dataset = '/home/markg/Documents/TCD/ML/ML1819--task-107--team-11/dataset/overall_dataset.csv'
    data = pd.read_csv(dataset, na_values = '?')

    # change appropriate variables to categorical. DON'T DO THIS!
    # data['gender'] = data['gender'].astype('category')
    # data['tweet_location'] = data['tweet_location'].astype('category')
    # data['user_timezone'] = data['user_timezone'].astype('float64')

    # reformat date column
    data['created'] = pd.to_datetime(data['created'])

    # create new columns for year and month
    data['year'] = pd.DatetimeIndex(data['created']).year
    data['month'] = pd.DatetimeIndex(data['created']).month

    # remove original date column
    data = data.drop(['created'], axis=1)

    # standardize numeric variables (could also consider using robust scaler here)
    numericVariables = ['fav_number', 'tweet_count','retweet_count', 'link_hue',
     'link_sat', 'link_vue', 'sidebar_hue', 'sidebar_sat', 'sidebar_vue', 'year', 'month']
    scaler = preprocessing.StandardScaler()
    data[numericVariables] = scaler.fit_transform(data[numericVariables])

    ##################### END SETUP CODE ######################################

    #################### SVM MODEL ############################################
    # # create dependent & independent variables
    # X = data.drop(['gender', 'fav_number', 'user_timezone', 'tweet_count','retweet_count', 'link_hue',
    #  'link_sat', 'link_vue', 'sidebar_sat', 'sidebar_vue', 'month'], axis=1)
    # # X = data.drop('gender', axis=1)
    # y = data['gender']
    # # print (X.keys())
    #
    #
    # # split into 90% training, 10% testing
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.10)
    #
    # # # train model (could change kernel here)
    # svm = SVC(C=1, gamma=0.3, kernel='rbf')
    # svm.fit(X_train, y_train)
    # #
    # # # # recursive feature selection using cross validation
    # # # rfecv = RFECV(estimator=svm, step=1, cv=StratifiedKFold(2),
    # # #               scoring='accuracy')
    # # # rfecv.fit(X, y)
    # # # print("Optimal number of features : %d" % rfecv.n_features_)
    # # # print("Feature ranking: ", rfecv.ranking_)

    # # # recursive feature selection without cross validation
    # rfe = RFE(svm, 3)
    # fit = rfe.fit(X, y)
    # print('Num Features:',fit.n_features_to_select)
    # print("Selected Features:",fit.support_)
    # #
    # plot bar chart of feature ranking
    features = list(X)
    ranking = rfecv.ranking_
    plt.bar(features, ranking, align='center', alpha=0.5)
    plt.show()

    # Plot number of features VS. cross-validation scores
    plt.figure()
    plt.xlabel("Number of features selected")
    plt.ylabel("Cross validation score (nb of correct classifications)")
    plt.plot(range(1, len(rfecv.grid_scores_) + 1), rfecv.grid_scores_)
    plt.show()
    #
    # make predictions and print metrics
    y_pred = svm.predict(X_test)
    print(classification_report(y_test,y_pred))
    print(confusion_matrix(y_test,y_pred))
    # #
    # # # # cross validation to choose c and gamma
    # C_s, gamma_s = np.meshgrid(np.logspace(-2, 1, 20), np.logspace(-2, 1, 20))
    # scores = list()
    # i=0; j=0
    # for C, gamma in zip(C_s.ravel(),gamma_s.ravel()):
    #     svm.C = C
    #     svm.gamma = gamma
    #     this_scores = cross_val_score(svm, X, y, cv=5)
    #     scores.append(np.mean(this_scores))
    # scores=np.array(scores)
    # scores=scores.reshape(C_s.shape)
    # fig2, ax2 = plt.subplots(figsize=(12,8))
    # c=ax2.contourf(C_s,gamma_s,scores)
    # ax2.set_xlabel('C')
    # ax2.set_ylabel('gamma')
    # fig2.colorbar(c)
    # fig2.savefig('crossvalOverall.png')

    ################## END SVM MODEL ##########################################

#     # create a subset of males and females
# #     males = data[data['gender']==0]
# #     females = data[data['gender']==1]
# #
# #     # to access specific columns
# #     favNumberMales = males.loc[:,'fav_number']
# #     favNumberFemales = females.loc[:,'fav_number']
# # #    plotHistTwo(favNumberMales, favNumberFemales)
# #
# #     tweetCountMales = males.loc[:,'tweet_count']
# #     tweetCountFemales = females.loc[:,'tweet_count']
#     # plotHistTwo(tweetCountMales, tweetCountFemales)
#
#     # retweetCountMales = males.loc[:,'retweet_count']
#     # retweetCountFemales = females.loc[:,'retweet_count']
#
#     # plot a histogram
#     #plot_hist(fav_number, "title", "favourited tweets", "freq")
#

    #################### LOGISTIC MODEL #######################################
    # create dependent & independent variables
    # X = data.drop('gender', axis=1)
    # Y = data['gender']
    #
    # model = LogisticRegression()
    # rfe = RFE(model, 3)
    # fit = rfe.fit(X, Y)
    # print('Num Features:',fit.n_features_to_select)
    # print("Selected Features:",fit.support_)
    #
    # # build model
    # logit_model=sm.Logit(Y,X)
    # result=logit_model.fit()
    #
    # X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
    # logreg = LogisticRegression()
    # logreg.fit(X_train, y_train)
    #
    # y_pred = logreg.predict(X_test)
    # # print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))
    # print(classification_report(y_test,y_pred))
    # # logit_roc_auc = roc_auc_score(y_test, logreg.predict(X_test))
    # # fpr, tpr, thresholds = roc_curve(y_test, logreg.predict_proba(X_test)[:,1])
    # # plt.figure()
    # # plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
    # # plt.plot([0, 1], [0, 1],'r--')
    # # plt.xlim([0.0, 1.0])
    # # plt.ylim([0.0, 1.05])
    # # plt.xlabel('False Positive Rate')
    # # plt.ylabel('True Positive Rate')
    # # plt.title('Receiver operating characteristic')
    # # plt.savefig('Log_ROC')
    # # plt.show()

    # to keep track of time taken
    endTIme = time.time()
    totalTime = endTIme - startTime
    print("Time taken:", totalTime)

if __name__ == '__main__':
  main()
