# Machine Learning Flask App on Google Kubernetes Engine with Load Test

This is the final project for a Duke Graduate level Cloud Analysis course.
Group Members: Xiaodi Nie, Yueyang Pan, Yuqiao Liang, Yijie Yan

## Titanic Passenger Survival Prediction

In this part, we used the [Titanic dataset](https://www.kaggle.com/c/titanic/data) and created a classification model using the Random Forests algorithm.

This dataset contains 891 training samples and 418 test samples with 11 features (PassengerId, Pclass, Name, Sex, Age, SibSp, Parch, Ticket, Fare, Cabin, Embarked). There are labels to indicate whether the passenger is survived or not in training data, but the test data do not have labels.

There are mainly 6 steps in the process of creating models:

1. Analyzing feature contributions
2. Data preprocessing (processing missing data and standardizing features)
3. Applying Random Forests to the model and evaluating performance using cross-validation and Out of Bag (OOB) score.
4. Analyzing feature importance for Random Forests and tuning parameters
5. Optimizing the model using the tuned parameters
6. Save the final model in the *Titanic_prediction_updated.joblib* file

The final model has a 92.26% training accuracy and 82.38% OOB score.
The model and dataset are under the *Titanic_model_prediction* folder.
All code, analysis, and model evaluations are presented in the *Titanic_prediction_updated.ipynb* file.

## Deploy Docker to Google Kubernetes Engine

After the model is pickled into a ```.joblib``` file, we can directly load it and run predictions from a simple flask app. We used Python3.6 in both the prediction model and the flask app.

The whole thing is wrapped inside a docker container, pushed to google container registry, then deployed on a Google Kubernetes Engine cluster. A load balancer was set up to expose a single endpoint, and behind it there were 6 duplicated pods(one pod basically contains one container) to better handle the traffic.

Follow this instruction to deploy and update: [Deploying a containerized web application](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app)


## Load test with Vegeta

[Vegeta](https://github.com/tsenart/vegeta) is a command line load testing tool written in Go. 


### Install Vegeta

You can directly download the pre-built binary or use brew to install if you're users of MacOS.

**Brew install**
```
brew update && brew install vegeta
```

**Download binary and unzip**

Find the latest release here: [Vegeta releases](https://github.com/tsenart/vegeta/releases)
```
wget https://github.com/tsenart/vegeta/releases/download/v7.0.3/vegeta-7.0.3-linux-amd64.tar.gz
tar xzvf vegeta-7.0.3-linux-amd64.tar.gz
mv vegeta  /usr/local/bin/
```

**Usage**

```vegeta --help```

See [Documents](https://github.com/tsenart/vegeta)

### Run load tests

In this project we have a endpoint provided by a load balancer directing traffic to the pods on the cluster, and the endpoint is expecting POST request with JSON payload. 

So we use this command to run the load test:
```
vegeta attack -targets=tmp -rate=1100 -duration=1.5s | tee results.bin | vegeta report
```
The POST request is in the ```tmp``` file and it looks like this:
```
POST http://[ENDPOINT]:8080/predict
Content-Type: application/json
@payload.json
```
The input data to the prediction model is in the ```payload.json``` file.

This test would generate 1100 requests/second and the output would look something like this:
```
ec2-user:~/environment/finalproject/loadtest (master) $ ./loadtest.sh 
Requests      [total, rate, throughput]         1650, 1100.75, 82.88
Duration      [total, attack, wait]             19.907s, 1.499s, 18.408s
Latencies     [min, mean, 50, 90, 95, 99, max]  158.774ms, 5.694s, 4.497s, 13.453s, 16.496s, 18.335s, 18.705s
Bytes In      [total, mean]                     75900, 46.00
Bytes Out     [total, mean]                     389400, 236.00
Success       [ratio]                           100.00%
Status Codes  [code:count]                      200:1650  
Error Set:
```

You can also check out the results in 3 ways:

1. Metrics

    ```vegeta report -type=json results.bin > metrics.json```
    
    This will include information regarding latencies, throughput, requests count, time stamp, etc.
    
2. Plot
    ```cat results.bin | vegeta plot > plot.html```

    This will generate a plot describing latency data:
    ![vegeta plot](/img/vegeta-plot.png)

3. Histogram 

    ```cat results.bin | vegeta report -type="hist[0,100ms,200ms,300ms]"```
    
    This will generate histogram about request count on specific time stamps:
    ```
    Bucket           #     %       Histogram
    [0s,     300ms]  11    0.67%   
    [300ms,  600ms]  22    1.33%   #
    [600ms,  900ms]  40    2.42%   #
    [900ms,  1.2s]   40    2.42%   #
    [1.2s,   +Inf]   1537  93.15%  #####################################################################
    ```
