#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
stats server:

Default Bind IP: localhost
Default Bind Port: 5090

The server listens on ports 5090 for any data.
Metric data should be of JSON format.
Mandatory keys:
'metric_name': A unqiue metric name
'metric_type': Type of Metric ('guage', 'trace', 'counter')
"""


class StatsServer(object):
    def __init__(self):
        pass

        
 def main():
     pass

 if __name__ == '__main__':
     main()
