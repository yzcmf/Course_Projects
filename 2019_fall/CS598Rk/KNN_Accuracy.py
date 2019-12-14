#!/usr/bin/env python
# coding: utf-8

# # KNN
# knn intro: https://www.cnblogs.com/fengfenggirl/archive/2013/05/27/knn.html

# In[1]:


import numpy as np
import pandas as pd
from pandas import concat
final_data = pd.read_csv("processed_data.csv")
unsplited_data = final_data.iloc[:, [1, 2, 3, 0]]
train_data = final_data.iloc[:49046, [1, 2, 3, 0]]
test_data = concat([final_data.iloc[0:0, [1, 2 , 3, 0]], final_data.iloc[49047:, [1 , 2, 3, 0]]])
print(train_data[:10])


# In[2]:


unsplited_data


# In[3]:


data = unsplited_data[1:].values
np.random.shuffle(data)


# In[4]:


data[:10]


# In[5]:


import hashlib
d1 = {}
def md5_1(s): 
    h = int(hashlib.md5(s.encode()).hexdigest(),16) / 1e29
    d1[h] = s  
    return h
d2 = {}
def md5_2(s): 
    h = int(hashlib.md5(s.encode()).hexdigest(),16) / 1e28
    d2[h] = s  
    return h 


# In[6]:


# https://www.bilibili.com/video/av64111297?p=46  
# in the video: (mutiply x => 2 outputs (0 or 1)) => supervised learning (46-49)
# in this problem: (mutiply x => mutiply y(unknown)) => unsupervised learning (156)
# KNN, Decision trees, SVM => https://www.geeksforgeeks.org/multiclass-classification-using-scikit-learn/
# https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression
a= data[::, :-1].tolist()
b= data[::, -1:].tolist()
# print(a[:3],'\n',len(a),'\n',type(a),'\n')
# print(b[:3],'\n',len(b),'\n',type(b),'\n')
a_ = []
for l in a:
    t = []
    for i in range(3): t.append(md5_1(l[i]))
    a_.append(t)
a = a_
b = [md5_2(item) for l in b for item in l]
# print(d1[15205963056818863091954712931819521019])
# print(d1[99396071082847217712602878136621166525])
# print(d2[140598361932073884279234491729198167766])
# data/1e28 => handle overflow error
x = np.asarray(a,dtype ='float64').reshape(-1,3)
y = np.asarray(b,dtype ='int64')
print(x[:10],'\n\n', y[:10])


# In[7]:


# # importing necessary libraries 
# from sklearn import datasets 
# from sklearn.metrics import confusion_matrix 
# from sklearn.model_selection import train_test_split 
  
# # loading the iris dataset 
# iris = datasets.load_iris() 
  
# # X -> features, y -> label 
# X = iris.data 
# Y = iris.target 
  
# # dividing X, y into train and test data 
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state = 0) 
  
# # training a DescisionTreeClassifier 
# from sklearn.tree import DecisionTreeClassifier 
# dtree_model = DecisionTreeClassifier(max_depth = 2).fit(X_train, Y_train) 
# dtree_predictions = dtree_model.predict(X_test) 
  
# # creating a confusion matrix 
# cm1 = confusion_matrix(Y_test, dtree_predictions) 


# In[8]:


# print(X.shape,Y.shape, type(X[0][0]), type(Y[0]))
# print(X[:5],Y[:5])
# print(Y_test, dtree_predictions)


# In[9]:


# print(38/150)
# print(Y_test.shape, dtree_predictions.shape)
# cm1


# In[10]:


# print(x.shape,y.shape, type(x[0][0]), type(y[0]))


# In[11]:


# # dividing X, y into train and test data 
# x1_train, x1_test, y1_train, y1_test = train_test_split(x, y, random_state = 0) 
  
# # training a DescisionTreeClassifier 
# from sklearn.tree import DecisionTreeClassifier 
# dtree_model1 = DecisionTreeClassifier(max_depth = 2).fit(x1_train, y1_train) 
# dtree_predictions1 = dtree_model1.predict(x1_test) 
  
# # creating a confusion matrix 
# cm2 = confusion_matrix(y1_test, dtree_predictions1) 


# In[12]:


# print(cm2.shape)
# cm2


# In[13]:


# print(y1_test.shape, dtree_predictions1.shape)
# l2 = cm2.tolist()
# for i in range(len(l2)):
#     for j in range(len(l2[i])):
#          if l2[i][j]:
#             print( i,j, l2[i][j] )


# In[14]:


# # importing necessary libraries 
# from sklearn import datasets 
# from sklearn.metrics import confusion_matrix 
# from sklearn.model_selection import train_test_split 
  
# # loading the iris dataset 
# iris = datasets.load_iris() 
  
# # X -> features, y -> label 
# X1 = iris.data 
# Y1 = iris.target 
  
# # dividing X, y into train and test data 
# X1_train, X1_test, Y1_train, Y1_test = train_test_split(X1, Y1, random_state = 0) 
  
# # training a linear SVM classifier 
# from sklearn.svm import SVC 
# svm_model_linear = SVC(kernel = 'linear', C = 1).fit(X1_train, Y1_train) 
# svm_predictions = svm_model_linear.predict(X1_test) 
  
# # model accuracy for X_test   
# accuracy = svm_model_linear.score(X1_test, Y1_test) 
  
# # creating a confusion matrix 
# cm3 = confusion_matrix(Y1_test, svm_predictions) 


# In[15]:


# print(X1.shape,Y1.shape, type(X1[0][0]), type(Y1[0]))


# In[16]:


# print(Y1_test.shape, svm_predictions.shape)
# cm3


# In[17]:


# # importing necessary libraries 
# from sklearn import datasets 
# from sklearn.metrics import confusion_matrix 
# from sklearn.model_selection import train_test_split 
  
# # dividing X, y into train and test data 
# x2_train, x2_test, y2_train, y2_test = train_test_split(x, y, random_state = 0) 
  
# # training a linear SVM classifier 
# from sklearn.svm import SVC 
# svm_model_linear = SVC(kernel = 'linear', C = 1).fit(x2_train, y2_train) 
# svm_predictions = svm_model_linear.predict(x2_test) 
  
# # model accuracy for X_test   
# accuracy = svm_model_linear.score(x2_test, y2_test) 
  
# # creating a confusion matrix 
# cm4 = confusion_matrix(y2_test, svm_predictions) 


# In[18]:


# print(x.shape,y.shape, type(x[0][0]), type(y[0]))


# In[19]:


# print(y2_test.shape, svm_predictions.shape)
# cm4
# l4 = cm4.tolist()
# for i in range(len(l4)):
#     for j in range(len(l4[i])):
#          if l4[i][j]:
#             print( i,j, l4[i][j] )


# In[20]:


# concatenate: http://lagrange.univ-lyon1.fr/docs/numpy/1.11.0/reference/generated/numpy.concatenate.html
from sklearn import datasets 
from sklearn.metrics import confusion_matrix 
from sklearn.model_selection import train_test_split 
from sklearn.neighbors import KNeighborsClassifier 
import copy
accuracy = 0
k = 0
# x_train, x_test, y_train, y_test = train_test_split(x, y, random_state = 0)
# x_ = copy.deepcopy(x_train)
# y_ = copy.deepcopy(y_train)
x_ = copy.deepcopy(x) # 65%
y_ = copy.deepcopy(y) # 65%
import time
timeout = time.time() + 30   # 30s from now
while accuracy < 1:
    k += 3000
#   M2 => improve the accuracy into ~ stable 95 - 99%
#   x3_train, x3_test, y3_train, y3_test = train_test_split(x_[:k], y_[:k], random_state = 0)
#   knn = KNeighborsClassifier(n_neighbors = 1).fit(x3_train, y3_train) # change from 7 to 1
    knn = KNeighborsClassifier(n_neighbors = 1).fit(x_[:k], y_[:k]) # change from 7 to 3
#   M1 => the accuracy into ~ unstable 80 - 99 %
    accuracy = knn.score(x_[:k], y_[:k]) 
    print(accuracy)
    knn_predictions = knn.predict(x_[:k])
    y_[:len(knn_predictions)] = knn_predictions
    if k + 3000 >= len(x_):
        x_ = np.concatenate((x_[k:], x_[:k]), axis=0) 
        y_ = np.concatenate((y_[k:], y_[:k]), axis=0) 
        k = 3000
    if time.time() > timeout: break


# In[21]:


# creating a confusion matrix 
knn_predictions = knn.predict(x)  
cm5 = confusion_matrix(y, knn_predictions) 


# In[22]:


print(y, knn_predictions)


# In[23]:


print(x.shape,y.shape, type(x[0][0]), type(y[0]))
print(y_.shape, knn_predictions.shape)
# print(cm5)
l5 = cm5.tolist()
c5 = 0
for i in range(len(l5)):
    mx =0 
    for j in range(len(l5[i])):
        mx = max(l5[i][j],mx)
#         if l5[i][j]:
#             print( i,j, l5[i][j] )
#         if l5[i][j] and i == j:
#             cnt += 1
#             print( i,j, l5[i][j] )
    if l5[i][i] == mx:
        c5 += 1
#         print(i, l5[i][i], mx)


# In[24]:


print(c5, len(l5))
print('accuracy = ', c5/len(l5))


# In[25]:


# accuracy on X_test 
accuracy1 = knn.score(x, y) 
print('original score = ', accuracy1)
# accuracy2 = knn.score(x_train, y_train) 
# print('train score =', accuracy2)
accuracy3 = knn.score(x_, y_) 
print('copy training phase score = ', accuracy3)


# In[26]:


# from sklearn import datasets 
# from sklearn.metrics import confusion_matrix 
# from sklearn.model_selection import train_test_split 

# # dividing X, y into train and test data 
# x4_train, x4_test, y4_train, y4_test = train_test_split(x, y, random_state = 0) 
  
# # training a Naive Bayes classifier 
# from sklearn.naive_bayes import GaussianNB 
# gnb = GaussianNB().fit(x4_train, y4_train) 
# gnb_predictions = gnb.predict(x4_test) 
  
# # accuracy on X_test 
# # accuracy = gnb.score(x4_test, y4_test) 
# # print(accuracy) 
  
# # creating a confusion matrix 
# cm6 = confusion_matrix(y4_test, gnb_predictions) 


# In[27]:


# print(x.shape,y.shape, type(x[0][0]), type(y[0]))
# print(y4_test.shape, gnb_predictions.shape)
# # print(cm6)
# l6 = cm6.tolist()
# c6 = 0
# for i in range(len(l6)):
#     mx = 0
#     for j in range(len(l6[i])):
#         mx = max(mx, l6[i][j])
# #          if l6[i][j]:
# #             print( i,j, l6[i][j] )
# #         if l6[i][j] and i == j:
# #             print( i,j, l6[i][j] )
#     if l6[i][i] == mx:
#         c6 += 1
# #         print(i, l6[i][i])


# In[28]:


# print(c6)
# print('accuracy = ', c6/len(l6))


# In[ ]:




