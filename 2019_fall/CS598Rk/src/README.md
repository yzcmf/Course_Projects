src code expalination

This is a task for mutli-class to multi-labels. At first, I used Linear Regression and it turns out no accuracy at all for this irregular dataset. Then I used other ways, especially for multi-labels preditions. I choose to use Decision-Tree, KNN, SVM and Naive Bayes classifier. I find KNN would mostly like to be a good fit for the dataset.

I first import panda, numpy and pyplot. I use panda to read csv file and do some data processing tasks. I get the final processed data which contains 3 class and we need to use them to predict about 1000 labels. One problem here is the input data is based on int and utf-8 and so that I used 2 md5 hash functions to cast all of them into float64.  

After getting the orginal_data, I build KNN model by using KNeighborsClassifier. In theory, we don't need training and testing data from KNN model. I first try not splited them and not training them with batch size, I get accuracy from 20 - 65 %. I then splited the data with batch size 75 % and 25%. One time I get the model, I used one batch size data as input and get the predictions from that input. I set the break time to be 90s or accuracy greater than 99% to break the while loop. Also, I used the score function to judage the accuracy.Based on processed dataset, we would have >70000 items and I set the batch size to be 3000. I could get the accuracy around 99% from the score function. 

After the KNN model, I used confused matrix and count the whole positive predictions , and obtained the finally accuracy to be 99.1% (72912 73567), while the confused matrix accuracy is 98.5% (837 850)

For the plot, due to the large size, we have to do the random sampling. I choose the random sampling 100,500,1000,2000 and have the finally results in the pretty-results folder. You could find when sample is 100 or 500, there are some inaccurate results and when the sample is 1000 or 2000, you could figure out the inaccurate results. However, we know there must be some inaccurate results there.

In the problem, I believe we could use Deep Learning methods and build deep networks such as CNN or RNN. I worry about its time cost here. In our case, there are only 3 class and therefore, the traditional machine learning methods are good enough to finish this job with a lower time cost.
