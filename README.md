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
