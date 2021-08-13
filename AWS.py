
import AWSIoTPythonSDK.MQTTLib as AWSIoT
import json

class AWS:
    # public
    topic = "/Oven"

    PATH_TO_CERT = "certificates/Oven.cert.pem"
    PATH_TO_KEY = "certificates/Oven.private.key"
    PATH_TO_ROOT = "certificates/root-CA.crt"
    # private
    client = None

    # inject
    main = None

    def __init__(self, main):
        self.main = main
        

        #<static values>
        ENDPOINT = "akyvbbf6sysh7-ats.iot.us-west-2.amazonaws.com"
        PORT = 443

        # AWSIoTMQTTClient credential configuration
        self.client = AWSIoT.AWSIoTMQTTClient(main.CLIENT_ID, useWebsocket=True)
        self.client.configureEndpoint(ENDPOINT, PORT)
        self.client.configureCredentials(self.PATH_TO_ROOT, self.PATH_TO_KEY, self.PATH_TO_CERT)
        
        # AWSIoTMQTTClient connection configuration
        self.client.configureAutoReconnectBackoffTime(1, 32, 20)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(6)  # 6 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec

        # Connect AWSIoTMQTTClient
        success = self.client.connect(10)
        if success:
            print("Connected...")
            # AWSIoTMQTTClient subscribe to incoming events
            self.client.subscribe(self.topic, 1, self.main.customCallback)
        else:
            print("Connection failed.")
            pass

    def publish(self, msg, val):
        data_msg = "{}".format(msg)
        data_val = "{}".format(val)
        if val is None:
            message = {"event" : data_msg, "value" : "{}".format(0)}
        else:
            message = {"event" : data_msg, "value" : data_val}
        success = self.client.publish(self.topic, json.dumps(message), 1)
        if success:
            print('Published: "' + str(message) + '" to topic "' + "'" + str(self.topic) + "'")
        else:
            print('Error publishing')

    def disconnect(self):
        try:
            self.client.disconnect()
        except:
            pass