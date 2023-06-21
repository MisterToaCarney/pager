FROM python:3.11-bookworm

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y gnuradio multimon-ng

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/usr/lib/python3/dist-packages/"

ENTRYPOINT [ "python", "./pager_monitor.py", "--nogui" ]
CMD ["--service-account", "/service_account.json", "--iio-context", "ip:192.168.1.31"]
