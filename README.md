# Pystatsd

A python daemon that listens for statistics like trace, counters, guages over UDP.
It aggregates to pluggable forwarder services - eg. (Kafka)


## Motivation:

Existing statsd implementation did not allow a way to pass additional tags when forwarding data to kafka.
Each metric name translates to individual table in influxdb.

This restriction causes clients to create separate metric names for every variation of the same metric type
which eventually explodes the number of tables in influxdb.

This statsd server implementation allows for additional tags to be passed by clients when forwarding metrics.



## Usage:
The pystatsd daemon listens on UDP port. It expects a json string and will drop data that does not match
the json format.


### pystatsd daemon/server setup:

Install Package:

```
[root@ip-sd]# ls pystatsd-1.0.0-1.x86_64.rpm 
pystatsd-1.0.0-1.x86_64.rpm
[root@ip-sd]# yum install pystatsd-1.0.0-1.x86_64.rpm 
Loaded plugins: fastestmirror
Examining pystatsd-1.0.0-1.x86_64.rpm: pystatsd-1.0.0-1.x86_64
Marking pystatsd-1.0.0-1.x86_64.rpm to be installed
Resolving Dependencies
--> Running transaction check
---> Package pystatsd.x86_64 0:1.0.0-1 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

=====================================================================================================================================================================================================
 Package                                     Arch                                      Version                                     Repository                                                   Size
=====================================================================================================================================================================================================
Installing:
 pystatsd                                    x86_64                                    1.0.0-1                                     /pystatsd-1.0.0-1.x86_64                                     52 k

Transaction Summary
=====================================================================================================================================================================================================
Install  1 Package

Total size: 52 k
Installed size: 52 k
Is this ok [y/d/N]: y
Downloading packages:
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
Collecting pyYAML==1.3.2
  Could not find a version that satisfies the requirement pyYAML==1.3.2 (from versions: 3.10, 3.11, 3.12)
No matching distribution found for pyYAML==1.3.2
You are using pip version 8.1.2, however version 9.0.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
Requirement already satisfied (use --upgrade to upgrade): PyYAML==3.10 in /usr/lib64/python2.7/site-packages
You are using pip version 8.1.2, however version 9.0.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
  Installing : pystatsd-1.0.0-1.x86_64                                                                                                                                                           1/1 
  Verifying  : pystatsd-1.0.0-1.x86_64                                                                                                                                                           1/1 

Installed:
  pystatsd.x86_64 0:1.0.0-1                                                                                                                                                                          

Complete!

```

Modify Config file (/etc/pystatsd/pystatsd.conf)

```
---
bind_address: "100.100.100.100"  <-- 127.0.0.1 if listening on localhost.
bind_port: 5090
debug_mode: False

agent:
    tags:
        environment: "stage"
        role: "cfbroker"

forwarders:
    kafka:
      kafka_broker: my-broker.url.abc.net:9092 
      kafka_topic: myKafkaTopic 
      kafka_apikey: 74444444444x6xxxxxxxxxxxxxxxxxxxxx
      kafka_tenant_id: xxxxxxxx69xxxxx69bcxxxxx1adxxxxx

```

Start the pystatsd server:

```
[root@ip-sd]# service pystatsd start
Redirecting to /bin/systemctl start  pystatsd.service
[root@ip-sd]# service pystatsd status
Redirecting to /bin/systemctl status  pystatsd.service
● pystatsd.service - LMM Logging API
   Loaded: loaded (/usr/lib/systemd/system/pystatsd.service; disabled; vendor preset: disabled)
   Active: active (running) since Tue 2017-03-21 16:34:34 UTC; 3s ago
 Main PID: 14645 (pystatsd)
   CGroup: /system.slice/pystatsd.service
           ├─14645 /bin/python /usr/bin/pystatsd
           ├─14646 /bin/python /usr/bin/pystatsd
           └─14647 /bin/python /usr/bin/pystatsd

Mar 21 16:34:34 ip- systemd[1]: Started LMM Logging API.
Mar 21 16:34:34 ip- systemd[1]: Starting LMM Logging API...
Mar 21 16:34:34 ip-symcpe.net pystatsd[14645]: Config Parsed!
Mar 21 16:34:34 ip-symcpe.net pystatsd[14645]: BRD: Run start
Mar 21 16:34:34 ip-symcpe.net pystatsd[14645]: UDP Server Started!
Mar 21 16:34:34 ip-symcpe.net pystatsd[14645]: Fowarder Started!
Mar 21 16:34:34 ip-symcpe.net pystatsd[14645]: [03-21-17 16:34  INFO MetricMgr]:  Initialized
Mar 21 16:34:34 ip-symcpe.net pystatsd[14645]: [03-21-17 16:34  INFO MetricMgr]:  TimerMonitor Initialized
Mar 21 16:34:34 ip-symcpe.net pystatsd[14645]: [03-21-17 16:34  INFO StatsForwarder]:  Initialized

[root@ip-sd]# ps -ef | grep python
root       706     1  0 Mar20 ?        00:00:07 /usr/bin/python -Es /usr/sbin/tuned -l -P
root     14645     1  0 16:34 ?        00:00:00 /bin/python /usr/bin/pystatsd
root     14646 14645  0 16:34 ?        00:00:00 /bin/python /usr/bin/pystatsd
root     14647 14645  0 16:34 ?        00:00:00 /bin/python /usr/bin/pystatsd
root     14662 14412  0 16:34 pts/0    00:00:00 grep --color=auto python


```

### pystats client:

Here are some examples (python clients), that send data to the statsd server:

```
udpsock = socket.socket(socket.AF_INET,
                        socket.SOCK_DGRAM)

def send_msg(msg):
    """Send message"""
    udpsock.sendto(msg, ('localhost', 5090))

# Trace
msg = {
    'metric_name': 'user.apptrace', 
    'metric_type': 'trace',
    'stage': 'Init app',
    'host': '192.44.2.2',
    'env': 'development'
}
send_msg(msg)

# Guage.
msg = {
    'metric_name': 'user.latency', 
    'metric_type': 'guage',
    'value': 4,4
    'stage': 'Init app',
    'host': '192.44.2.2',
    'env': 'development'
}
send_msg(msg)
```


## Building a Debian Package:

To build a debian package run:

```
./tools/build_deb.sh

``` 

## Building an RPM Package

To build an RPM package run:

```
./tools/build_rpm.sh

```



## License

Copyright 2015 Symantec Corporation.

Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License.

You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
