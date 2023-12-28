FROM archlinux:latest

RUN pacman -Syyu --noconfirm && pacman-db-upgrade

RUN mkdir /app
WORKDIR /app
COPY . .

RUN pacman -S --noconfirm multimon-ng gnuradio python qwt python-pip
RUN pip install --break-system-packages -r requirements.txt

CMD [ "/app/pager_monitor.py", "--nogui", "--service-account", "/app/firebase_key.json", "--iio-context", "ip:192.168.1.31" ]