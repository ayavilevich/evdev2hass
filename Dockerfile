# FROM python:3.10-slim-buster
FROM python:3.10-buster

ADD evdev2hass.py .

RUN pip install requests

# Install python evdev
RUN pip install requests evdev

# ENTRYPOINT [ "./evdev2hass.py" ]
ENTRYPOINT [ "python3", "./evdev2hass.py" ]
