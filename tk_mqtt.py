import paho.mqtt.client as mqtt #import the client1
from tkinter import *
from PIL import ImageTk, Image
from pathlib import Path
# Constants
DOOR_OPEN = 0
DOOR_CLOSED = 1
DOOR_UNKNOWN =2

#Get the window and set the size
window = Tk()
window.geometry('680x480')

#Load the images
path = str((Path(r'/home/pi/garagePimon/tests'))) + '/'
print(path)
img_open = ImageTk.PhotoImage(Image.open(path + "green.jpg"))
img_closed = ImageTk.PhotoImage(Image.open(path + 'blue.jpg'))
img_unknown =ImageTk.PhotoImage(Image.open(path + 'red.jpg'))

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
        panel.configure(image=img_closed)
        print("****ON")
        panel.update()
    #If the received message is light off then set the image the the ‘light off’ image
    elif doorstate == DOOR_CLOSED:
        panel.configure(image=img_open)
        print("****OFF")
        panel.update()
    else:
        panel.configure(image=img_unknown)


broker_address="10.211.1.127"

print("creating new instance")
client = mqtt.Client() #create new instance
client.on_message=on_message #attach function to callback

print("connecting to broker")
client.connect(broker_address) #connect to broker

topic = "door_distance"
print("Subscribing to topic " + topic)
client.subscribe(topic)

 #Start the MQTT Mosquito process loop
client.loop_start()

def on_closing():
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()