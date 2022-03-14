#! /usr/bin/python3

# capture evdev events and send to hass API as events
# reference:
# https://www.home-assistant.io/integrations/keyboard_remote/
# https://developers.home-assistant.io/docs/api/rest/
# https://docs.python-requests.org/en/master/

import evdev
import argparse
import os
import sys
from requests import post

valueToAction = ['release', 'press', 'hold']

def loop(identity, device, endpoint, token):
	dev = evdev.InputDevice(device)
	dev.grab()
	print("Grabbing", dev)
	# print(dev.capabilities(verbose=True))

	for event in dev.read_loop():
		# interesting properties: type (key, etc), code (scan code), value (up, down, hold)
		if event.type == evdev.ecodes.EV_KEY:
			key = evdev.ecodes.KEY[event.code]
			# some reverse mapping can point to more than one entry
			if type(key) is list:
				key = key[0]

			# debug
			print(event.type, event.code, event.value, key)

			# call API
			payload = {
				# https://stackoverflow.com/questions/4271740/how-can-i-use-python-to-get-the-system-hostname
				'identity': identity,
				'device': device,
				# 'eventType': event.type,
				'eventTimeSec': event.sec,
				'eventCode': event.code,
				'eventValue': event.value,
				'action': valueToAction[event.value],
				'key': key
			}
			url = endpoint + "events/evdev"
			headers = {
				"Authorization": "Bearer " + token,
				"content-type": "application/json",
			}

			try:
				response = post(url, headers=headers, json=payload)
				print(response.status_code, response.text)
				response.raise_for_status()
			except:
				e = sys.exc_info()[0]
				print(e)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description='evdev2mqtt -- Evdev to MQTT Gateway')
	parser.add_argument("-e", "--endpoint",
						dest="endpoint",
						default="http://hassio.lan:8123/api/",
						help="HASS API end-point")
	parser.add_argument("-t", "--token",
						dest="token",
						default="",
						required=True,
						help="HASS API authentication token")
	parser.add_argument("-d", "--device",
						dest="device",
						default="/dev/input/event1",
						help="Path to the evdev device")
	parser.add_argument("-i", "--identity",
						dest="identity",
						default=os.uname()[1],
						help="Idnetity of this script/container")
	args = parser.parse_args()

	loop(args.identity, args.device, args.endpoint, args.token)
