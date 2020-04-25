# ML-model-on-GKE-with-load-test

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

In this project we have a endpoint provided by a load balancer directing traffic to 3 pods running on a Google Kubernetes cluster, and the endpoint is expecting POST request with JSON payload. 

So we use this command to run the load test:
```
vegeta attack -targets=tmp -rate=1100 -duration=1s | tee results.bin | vegeta report
```
The POST request is in the ```tmp``` file and it looks like this:
```
POST http://35.243.217.145:80/predict
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
    [0s,     200ms]  4     0.37%   
    [200ms,  400ms]  22    2.01%   #
    [400ms,  600ms]  18    1.64%   #
    [600ms,  800ms]  21    1.92%   #
    [800ms,  +Inf]   1030  94.06%  ######################################################################
    ```