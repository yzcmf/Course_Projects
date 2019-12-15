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


a= data[::, :-1].tolist()
b= data[::, -1:].tolist()
a_ = []
for l in a:
    t = []
    for i in range(3): t.append(md5_1(l[i]))
    a_.append(t)
a = a_
b = [md5_2(item) for l in b for item in l]
x = np.asarray(a,dtype ='float64').reshape(-1,3)
y = np.asarray(b,dtype ='int64')
print(x[:10],'\n\n', y[:10])


# In[7]:


from sklearn import datasets 
from sklearn.metrics import confusion_matrix 
from sklearn.model_selection import train_test_split 
from sklearn.neighbors import KNeighborsClassifier 
import copy
accuracy = 0
k = 0
x_ = copy.deepcopy(x)
y_ = copy.deepcopy(y)
import time
timeout = time.time() + 90   # 90s from now
while accuracy < 0.99:
    k += 3000
    x3_train, x3_test, y3_train, y3_test = train_test_split(x_[:k], y_[:k], random_state = 0)
    knn = KNeighborsClassifier(n_neighbors = 1).fit(x3_train, y3_train)
    accuracy = knn.score(x_[:k], y_[:k]) 
    print(accuracy)
    knn_predictions = knn.predict(x_[:k])
    y_[:len(knn_predictions)] = knn_predictions
    if k + 3000 >= len(x_):
        x_ = np.concatenate((x_[k:], x_[:k]), axis=0) 
        y_ = np.concatenate((y_[k:], y_[:k]), axis=0) 
        k = 3000
    if time.time() > timeout: break


# In[8]:


# confusion matrix https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
labels = list(d2.values())
knn_predictions = knn.predict(x_)  
cm5 = confusion_matrix(y_, knn_predictions) 
# knn_predictions = knn.predict(x)  
# cm5 = confusion_matrix(y, knn_predictions)


# In[9]:


print(y_, knn_predictions)
# print(y, knn_predictions)


# In[10]:


print(x.shape,y.shape, type(x[0][0]), type(y[0]))
print(y_.shape, knn_predictions.shape)
l5 = cm5.tolist()
print(len(l5))
c5 = 0
c6 = 0
out = []
for i in range(len(l5)):
    mx_i = l5[i][i]
    mx = 0 
    for j in range(len(l5[i])): mx = max(l5[i][j],mx)
    if mx_i == mx:
        c5 += 1
        c6 += mx
        out.append((i,mx))
#         if l5[i][i] > 1097: print(l5[i][i], mx, i)
#         print(i, l5[i][i], mx)


# In[11]:


print(c5, len(l5))
print('matrix accuracy = ', c5/len(l5))
print(c6, len(y_))
print('orginal accuracy = ', c6/len(y_))


# In[12]:


accuracy1 = knn.score(x, y) 
print('original score = ', accuracy1)
accuracy2 = knn.score(x_, y_) 
print('copy training phase score = ', accuracy2)


# In[13]:


print(out[:10])


# In[14]:


print(len(out),len(labels))
print(out[8])
for i in range(10):
    print("%d:%s:%r" % (i, labels[out[i][0]].center(1), out[i][0] == out[i][1]) ) 


# In[15]:


c1 = 0
for v in y_- knn_predictions:
    if v == 0: c1 += 1
print('orginal accuracy= ', c1/len(y_))


# In[39]:


from matplotlib import pyplot as plt
plt.figure()
plt.title('Figure1')
plt.subplot(511)
plt.title('org100')
plt.plot(y_[::100], 'mo')
plt.subplot(513)
plt.title(' pred-100')
plt.plot(knn_predictions[::100], 'go')
plt.subplot(515)
plt.title('diff-100')
plt.plot(y_[::100] - knn_predictions[::100], 'bo')
plt.show()


# In[40]:


plt.figure()
plt.title('Figure1')
plt.subplot(511)
plt.title('org500')
plt.plot(y_[::500], 'mo')
plt.subplot(513)
plt.title(' pred-500')
plt.plot(knn_predictions[::500], 'go')
plt.subplot(515)
plt.title('diff-500')
plt.plot(y_[::500] - knn_predictions[::500], 'bo')
plt.show()


# In[37]:


plt.figure()
plt.title('Figure1')
plt.subplot(511)
plt.title('org1000')
plt.plot(y_[::1000], 'mo')
plt.subplot(513)
plt.title(' pred-1000')
plt.plot(knn_predictions[::1000], 'go')
plt.subplot(515)
plt.title('diff-1000')
plt.plot(y_[::1000] - knn_predictions[::1000], 'bo')
plt.show()


# In[38]:


plt.figure()
plt.title('Figure1')
plt.subplot(511)
plt.title('org2000')
plt.plot(y_[::2000], 'mo')
plt.subplot(513)
plt.title(' pred-2000')
plt.plot(knn_predictions[::2000], 'go')
plt.subplot(515)
plt.title('diff-2000')
plt.plot(y_[::2000] - knn_predictions[::2000], 'bo')
plt.show()


# In[17]:


# Unpassed raw data
knn_predictions0 = knn.predict(x)
c2 = 0
for v in y - knn_predictions0:
    if v == 0: c2 += 1
print('orginal accuracy0= ', c2/len(y))

