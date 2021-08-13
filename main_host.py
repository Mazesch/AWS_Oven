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
from yakindu.rx import Observer

import timer_service as m_TimerService
import Oven as m_Oven
import statechart as m_Statechart
import Gui as m_Gui
import AWS as m_AWS




class Main:
    CLIENT_ID = "oven"
    aws = None
    statechart = None
    oven = None
    running = True

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
        # Initialize Oven
        self.oven = m_Oven.Oven()


        # Initialize Statechart
        self.statechart = m_Statechart.Statechart()

        # Initialize Timerservice (required for Cyclebased statecharts)
        self.statechart.timer_service = m_TimerService.TimerService()

        # Initialize and set Callback of statechart in-events
        callback = Callback(self.statechart, self.oven)
        self.statechart.operation_callback = callback   


        # Initialize Gui
        self.gui = m_Gui.Gui(self)
        

        # Initialize AWS
        self.aws = m_AWS.AWS(self)


        # Set statechart observer for out-events
        class Reached_Temperature_Observer( Observer ):
            def __init__(self, aws):
                self.aws = aws
            def next(self, value=None):
                if self.aws is not None:
                    self.aws.publish("reachedTemperature", None)
                else:
                    print("Could not publish '" + "reachedTemperature" + "' because not connection was established.")  
        reached_temperature_observer = Reached_Temperature_Observer(self.aws)
        self.statechart.ready_observable.subscribe(reached_temperature_observer)

        class Cooled_Down_Observer( Observer ):
            def __init__(self, aws):
                self.aws = aws
            def next(self, value=None):
                if self.aws is not None:
                    self.aws.publish("cooledDown", None)
                else:
                    print("Could not publish '" + "cooledDown" + "' because not connection was established.")
        cooled_down_observer = Cooled_Down_Observer(self.aws)
        self.statechart.off_observable.subscribe(cooled_down_observer)

        # Enter statechart (required!)
        self.statechart.enter()

    # update all required objects
    def update(self, dt):
        self.statechart.run_cycle()
        self.oven.update(dt)
        keep_running = self.gui.update(dt)
        return keep_running

    # exit function and cleanup
    def exit(self):
        self.aws.disconnect()
        self.gui.close()
        os._exit(0)
    
    def getTemp(self):
        return self.oven.temperature

    def raise_set_target_temp(self, value, shouldPublish):
        self.statechart.raise_set_target_temp(value)
        self.gui.setNewTemp(value)
        if shouldPublish:
            time.sleep(0.1)
            self.aws.publish("setTargetTemperature", value)

    def customCallback(self, client, userdata, message):
        dictionary = json.loads(message.payload)
        if dictionary["event"] and dictionary["value"]:
            if dictionary["event"] == "setTargetTemperature":
                value = float(dictionary["value"])
                self.raise_set_target_temp(value, False)
            print('Received: "' + str(json.loads(message.payload)) + '" from topic "' + "'" + (message.topic) + "'")
            
# Class for defining callbacks for statechart out-events
class Callback:
    statechart = None
    oven = None

    def __init__(self, statechart, oven):
        self.statechart = statechart
        self.oven = oven

    def heat_on(self):
        self.oven.heatOn()
    
    def heat_off(self):
        self.oven.heatOff()
    
    def get_temp(self):
        return self.oven.getTemp()



# helper function to get current milliseconds
def current_milli_time():
    return round(time.time() * 1000)


# main entry point
if __name__ == "__main__":
    Main()