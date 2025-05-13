FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    usbip \
    libusb-1.0-0 \
    iproute2 \
    && apt-get clean

WORKDIR /app
COPY . /app/
COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["python", "app.py"]
