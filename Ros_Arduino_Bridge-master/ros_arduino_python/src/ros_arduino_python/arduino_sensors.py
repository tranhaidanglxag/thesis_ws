#!/usr/bin/env python

"""
    Sensor class for the arudino_python package
    
    Created for the Pi Robot Project: http://www.pirobot.org
    Copyright (c) 2012 Patrick Goebel.  All rights reserved.

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:
    
    http://www.gnu.org/licenses/gpl.html
"""

import roslib; roslib.load_manifest('ros_arduino_python')
import rospy
from geometry_msgs.msg import Point32
from sensor_msgs.msg import Range, PointCloud
from ros_arduino_msgs.msg import *

LOW = 0
HIGH = 1

INPUT = 0
OUTPUT = 1
    
class MessageType:
    ANALOG = 0
    DIGITAL = 1
    RANGE = 2
    FLOAT = 3
    INT = 4
    BOOL = 5
    POINTCLOUD = 6
    
class Sensor(object):
    def __init__(self, controller, name, pin, echopin, rate, frame_id="sensor_base", direction="input", **kwargs):
        self.controller = controller
        self.name = name
        self.pin = pin
        self.echopin = echopin
        self.rate = rate
        self.direction = direction

        self.frame_id = frame_id
        self.value = None
        
        self.t_delta = rospy.Duration(1.0 / self.rate)
        self.t_next = rospy.Time.now() + self.t_delta
    
    def poll(self):
        now = rospy.Time.now()
        if now > self.t_next:
            if self.direction == "input":
                try:
                    self.value = self.read_value()
                except:
                    return
            else:
                try:
                    self.ack = self.write_value()
                except:
                    return          
    
            # For range sensors, assign the value to the range message field
            if self.message_type == MessageType.RANGE:
                self.msg.range = self.value
            elif self.message_type == MessageType.POINTCLOUD: 
                #empty list first
                del self.msg.points[:] 
                #one sensor has a width of 30 degrees; i.e. formula for width of beam is 30/360 * 2*pi*distance ~= 0.6*distance
                #number of points on sonar arc
                MAX_SENSOR_POINTS = 5
                for index in range(MAX_SENSOR_POINTS):
                        newPoint = Point32()
                        newPoint.x = self.value
	                newPoint.y = -self.value*0.3 + index*self.value*0.3/(MAX_SENSOR_POINTS/2)
	                newPoint.z = 0.0               
                        self.msg.points.append(newPoint)         
            else:
                self.msg.value = self.value

            # Add a timestamp and publish the message
            self.msg.header.stamp = rospy.Time.now()
            self.pub.publish(self.msg)
            
            self.t_next = now + self.t_delta
    
class AnalogSensor(Sensor):
    def __init__(self, *args, **kwargs):
        super(AnalogSensor, self).__init__(*args, **kwargs)
                
        self.message_type = MessageType.ANALOG
        
        self.msg = Analog()
        self.msg.header.frame_id = self.frame_id
        
        self.pub = rospy.Publisher("~sensor/" + self.name, Analog)
        
        if self.direction == "output":
            self.controller.pin_mode(self.pin, OUTPUT)
        else:
            self.controller.pin_mode(self.pin, INPUT)

        self.value = LOW
        
    def read_value(self):
        return self.controller.analog_read(self.pin)
    
    def write_value(self, value):
        return self.controller.analog_write(self.pin, value)
    
class AnalogFloatSensor(Sensor):
    def __init__(self, *args, **kwargs):
        super(AnalogFloatSensor, self).__init__(*args, **kwargs)
                
        self.message_type = MessageType.ANALOG
        
        self.msg = AnalogFloat()
        self.msg.header.frame_id = self.frame_id
        
        self.pub = rospy.Publisher("~sensor/" + self.name, AnalogFloat)
        
        if self.direction == "output":
            self.controller.pin_mode(self.pin, OUTPUT)
        else:
            self.controller.pin_mode(self.pin, INPUT)

        self.value = LOW
        
    def read_value(self):
        return self.controller.analog_read(self.pin)
    
    def write_value(self, value):
        return self.controller.analog_write(self.pin, value)
    
        
class DigitalSensor(Sensor):
    def __init__(self, *args, **kwargs):
        super(DigitalSensor, self).__init__(*args, **kwargs)
        
        self.message_type = MessageType.BOOL
        
        self.msg = Digital()
        self.msg.header.frame_id = self.frame_id
        
        self.pub = rospy.Publisher("~sensor/" + self.name, Digital)
        
        if self.direction == "output":
            self.controller.pin_mode(self.pin, OUTPUT)
        else:
            self.controller.pin_mode(self.pin, INPUT)

        self.value = LOW
        
    def read_value(self):
        return self.controller.digital_read(self.pin)
    
    def write_value(self):
        # Alternate HIGH/LOW when writing at a fixed rate
        self.value = not self.value
        return self.controller.digital_write(self.pin, self.value)
    
class PointCloudRangeSensor(Sensor):
    def __init__(self, *args, **kwargs):
        super(PointCloudRangeSensor, self).__init__(*args, **kwargs)
        
        self.message_type = MessageType.POINTCLOUD
        
        self.msg = PointCloud()
        self.msg.header.frame_id = self.frame_id
        self.msg.points = []
        self.pub = rospy.Publisher("~sensor/" + self.name, PointCloud, queue_size=5)
        
    def read_value(self):
        self.msg.header.stamp = rospy.Time.now()    
class RangeSensor(Sensor):
    def __init__(self, *args, **kwargs):
        super(RangeSensor, self).__init__(*args, **kwargs)
        
        self.message_type = MessageType.RANGE
        
        self.msg = Range()
        self.msg.header.frame_id = self.frame_id
        
        self.pub = rospy.Publisher("~sensor/" + self.name, Range,queue_size=5)
        
    def read_value(self):
        self.msg.header.stamp = rospy.Time.now()

        
class SonarSensor(RangeSensor):
    def __init__(self, *args, **kwargs):
        super(SonarSensor, self).__init__(*args, **kwargs)
        
        self.msg.radiation_type = Range.ULTRASOUND
        
        
class IRSensor(RangeSensor):
    def __init__(self, *args, **kwargs):
        super(IRSensor, self).__init__(*args, **kwargs)
        
        self.msg.radiation_type = Range.INFRARED
        
class Ping(SonarSensor):
    def __init__(self,*args, **kwargs):
        super(Ping, self).__init__(*args, **kwargs)
                
        self.msg.field_of_view = 0.785398163
        self.msg.min_range = 0.02
        self.msg.max_range = 5.0
        
    def read_value(self):
        # The Arduino Ping code returns the distance in centimeters
        cm = self.controller.ping(self.pin, self.echopin)
        
        # Convert it to meters for ROS
        distance = cm / 100.0
        
        return distance
class PointCloudPing(PointCloudRangeSensor):
    def __init__(self,*args, **kwargs):
        super(PointCloudPing, self).__init__(*args, **kwargs)
     
    def read_value(self):
        # The Arduino Ping code returns the distance in centimeters
        cm = self.controller.ping(self.pin, self.echopin)
        
        # Convert it to meters for ROS
        distance = cm / 100.0
        return distance
    
            
if __name__ == '__main__':
    myController = Controller()
    mySensor = SonarSensor(myController, "My Sonar", type=Type.PING, pin=0,rate=10)
            