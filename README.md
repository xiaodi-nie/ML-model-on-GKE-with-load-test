# ML-model-on-GKE-with-load-test

## Titanic Prediction Model

## Deploy Docker to Google Kubernetes Engine

After the model is pickled we can directly load it and run predictions from a simple flask app. We used Python3.6 in both the prediction model and the flask app.

The whole thing is wrapped inside a docker container, pushed to google container registry, then deployed on a GKE cluster. A load balancer was set up to expose a single endpoint, and behind it there were 6 duplicated pods to better handle the traffic.

Follow this instruction: [Deploying a containerized web application](https://cloud.google.com/kubernetes-engine/docs/tutorials/hello-app)


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

This test would generate 1100 requests/second and you can check out the results in 3 ways:

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
