# AWS Oven

This project is linked to the article at [Embedded Artistry](https://embeddedartistry.com).

## Description

This project contains two main files: `main_host.py` and `main_client.py`.
`main_host.py` connects a simulated IoT oven to the AWS Broker and allows displaying and setting the temperature of the oven.
`main_client.py` also connects to a simulated IoT oven, but can only set the temperature and display the general state of the oven.

To run these a folder called `certificates` needs to be created with the appropriate certificate files from AWS.
The variable `ENDPOINT` in `AWS.py` also needs to be changed to fit your endpoint.

## Getting Started

### Dependencies
* PySimpleGUI
* AWSIoTPythonSDK

### Executing program

* python /path/to/main_host.py
* python /path/to/main_client.py

## Authors

Mathias Schulte
Email: mschulte@itemis.com
