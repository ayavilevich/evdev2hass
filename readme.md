# A small Python script in a docker container to send keyboard events from a linux device to Home Assistant

For example, you can use a USB keyboard/keypad connected to a Raspberry Pi to trigger automations in your HASS based Smart Home.

https://en.wikipedia.org/wiki/Evdev - evdev (short for 'event device') is a generic input event interface in the Linux kernel and FreeBSD.

The keyboard events are sent into HASS as events of type ``evdev``. You can setup such events as triggers for automations.

Example of event data in HASS:

```
{
    "event_type": "evdev",
    "data": {
        "identity": "raspi2",
        "device": "/dev/input/event1",
        "eventTimeSec": 1647268288,
        "eventCode": 7,
        "eventValue": 0,
        "action": "release",
        "key": "KEY_6"
    },
    "origin": "REMOTE",
    "time_fired": "2022-03-14T14:31:28.217694+00:00",
    "context": {
        "id": "xxxxxxxxxxxxxxxxxxxxxxxxx",
        "parent_id": null,
        "user_id": "xxxxxxxxxxxxxxxxxxxxxxxx"
    }
}
```

The docker file is written for Raspbian Buster, but can be adapted to other distributions as well.

If your keyboard is directly connected to the HASS machine then this is not the right software for you. Use https://www.home-assistant.io/integrations/keyboard_remote/ instead.

This project is for use cases where you have a keyboard or possibly a small 4, 6, 10 button USB keypad that you want to use as a physical control pad for your smart home and when that device is connected to a different machine than the one running your HASS.

See ``evdev2hass.py`` for supported command line parameters.

## Useful docker commands

```
docker image build -t python-evdev2hass .
docker images

https://stackoverflow.com/questions/24225647/docker-a-way-to-give-access-to-a-host-usb-or-serial-device

docker run -t -i --init --privileged python-evdev2hass -i <identity> -t <hass token>

docker ps
docker stop <name>

docker rm evdev2hass
docker run -d --name evdev2hass --init --restart unless-stopped --privileged python-evdev2hass -i <identity> -t <hass token>
docker stop evdev2hass

docker image prune -a
```
