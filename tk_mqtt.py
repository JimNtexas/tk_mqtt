import paho.mqtt.client as mqtt #import the client1
from tkinter import *
from PIL import ImageTk, Image
from pathlib import Path
import socket
import time
import sys

# Constants
DOOR_OPEN = 0
DOOR_CLOSED = 1
DOOR_UNKNOWN =2

broker_address="10.211.1.127"
broker_port = 1883

# November 2023 update

def is_broker_available(broker_address, broker_port):
    try:
        # Create a socket object
        s = socket.create_connection((broker_address,broker_port), 5)
        s.close()  # Close the socket
        return True
    except:
        return False

while not is_broker_available(broker_address,broker_port ):
    result = messagebox.askretrycancel("Communications problem", "garage signal not found")
    if result:
        continue
    else: 
        sys.exit("Please check garage sensor")

#Get the window and set the size
window = Tk()
window.geometry('680x480')


#Load both the images
path = str((Path('Doorcheck'))) + '/'

pathpath = str(Path.home()) + '/Doorcheck/'

print(pathpath)
img_closed = ImageTk.PhotoImage(Image.open('green.jpg'))
img_unknown =ImageTk.PhotoImage(Image.open('red.jpg'))
img_open = ImageTk.PhotoImage(Image.open('blue.jpg'))

var = StringVar()
var.set("Garage Door Status")
panel = Label(window, image = img_unknown,textvariable=var,relief=RAISED)
panel.pack(side = "bottom", fill = "both", expand = "yes")


def get_state(distance):
    if((distance <= 13.5) and distance > 0):
        return DOOR_OPEN
    elif(distance > 13.5):
        return DOOR_CLOSED
    else:
        return DOOR_UNKNOWN

# This is the event handler method that receives the Mosquito messages
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    print("message received " , msg)
    doorstate = get_state(float(msg))
    #If the received message is light on then set the image the the ‘light on’ image
    if doorstate == DOOR_OPEN:
        panel.configure(image=img_open)
        print("****open")
        panel.update()
    #If the received message is light off then set the image the the ‘light off’ image
    elif doorstate == DOOR_CLOSED:
        panel.configure(image=img_closed)
        print("****closed")
        panel.update()
    else:
        panel.configure(image=img_unknown)
        print("****unknown")


print("creating new instance")
client = mqtt.Client() #create new instance
client.on_message=on_message #attach function to callback

while True:
    print("connecting to broker")
    try:
        client.connect(broker_address)  # connect to broker
        print("Connected to broker")
        break  # exit the loop if connection is successful
    except mqtt.MQTTException as e:
        print(f"Error connecting to broker: {e}")
        print("Retrying in 5 seconds...")
        time.sleep(5)

topic = "door_distance"
print("Subscribing to topic " + topic)
client.subscribe(topic)

 #Start the MQTT Mosquito process loop
client.loop_start()

def on_closing():
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
