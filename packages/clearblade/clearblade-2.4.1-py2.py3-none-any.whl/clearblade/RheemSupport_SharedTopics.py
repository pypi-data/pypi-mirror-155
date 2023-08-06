from clearblade.ClearBladeCore import System
import time

# System credentials
SystemKey = "a4d1dddf0b84f1b584dbb5dfbcf801"
SystemSecret = "A4D1DDDF0BB69499B899ADB5A4FB01"

mySystem = System(SystemKey, SystemSecret, "https://platform.clearblade.com")

user = mySystem.User("b@b.b", "b")
mqtt = mySystem.Messaging(user)

# Set up callback functions
def on_connect(client, userdata, flags, rc):
    client.subscribe("$share/yo/a/b/c")

def on_message(client, userdata, message):
    # When we receive a message, print it out
    print (f"Received message {message.payload} on topic {message.topic}.")

# Connect callbacks to client
mqtt.on_connect = on_connect
mqtt.on_message = on_message

# Connect and wait for messages
mqtt.connect()
while(True):
    time.sleep(1)  # wait for messages