"""
Example message for calling the setTargetTemperature in-event

TOPIC:"/Oven/in_events"

MESSAGE:"{
  "event": "setTargetTemperature",
  "value": "10.0"
}"
"""

import sys
import time
import os
import json

import Gui as m_Gui
import AWS as m_AWS

class Main:
    CLIENT_ID = "oven_controller"

    aws = None
    statechart = None
    oven = None
    running = True
    currentStatus = "Current status is off."

    def __init__(self):
        self.load()
        self.last_update = current_milli_time()
        self.running = True
        while(self.running):
            dt = (current_milli_time() - self.last_update)/1000
            self.last_update = current_milli_time()
            self.running = self.update(dt)
        self.exit()

    def load(self):
        # Initialize Gui
        self.gui = m_Gui.Gui(self)
        
        # Initialize AWS
        self.aws = m_AWS.AWS(self)

    # update all required objects
    def update(self, dt):
        keep_running = self.gui.update(dt)
        self.gui.setCurrent(self.currentStatus)
        return keep_running

    # exit function and cleanup
    def exit(self):
        self.aws.disconnect()
        self.gui.close()
        os._exit(0)

    
    def getTemp(self):
        return 0

    def raise_set_target_temp(self, value, shouldPublish):
        self.gui.setNewTemp(value)
        if shouldPublish:
            self.aws.publish("setTargetTemperature", value)

    def customCallback(self, client, userdata, message):
        dictionary = json.loads(message.payload)
        if dictionary["event"] and dictionary["value"]:
            if dictionary["event"] == "setTargetTemperature":
                value = float(dictionary["value"])
                self.currentStatus = "Current status is changing to " + str("{:.2f}".format(value)) + "ºC."
                self.raise_set_target_temp(value, False)
            if dictionary["event"] == "reachedTemperature":
                self.currentStatus = "Current status is 'reachedTemperature'."
            if dictionary["event"] == "cooledDown":
                self.currentStatus = "Current status is 'cooledDown'."
            print('Received: "' + str(json.loads(message.payload)) + '" from topic "' + "'" + (message.topic) + "'")


# helper function to get current milliseconds
def current_milli_time():
    return round(time.time() * 1000)


# main entry point
if __name__ == "__main__":
    Main()