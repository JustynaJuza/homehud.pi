# How to deploy on Pi
##### Prepare source folder
Copy source via WinSCP.

#### SSH to Pi.
Obtain Pi IP, e.g. log in to your router and list devices to find IP.
```sh
ssh admin@192.rest.of.ip
```

##### Prepare service file
Create a service unit file - **HomeHUDPi.service** file is included.
Set permission on service file.
```sh
$ sudo vim /lib/systemd/system/HomeHUDPi.service
$ sudo chmod 644 /lib/systemd/system/myscript.service
```
##### Make Pi aware of service
Register service with systemctl:
```sh
$ sudo systemctl daemon-reload
$ sudo systemctl enable myscript.service
```
##### See it work
Reboot Pi, service should run after boot. Check status of running service.
```sh
$ sudo reboot
$ sudo systemctl status HomeHUDPi.service
```
##### Stop and start if needed
```sh
$ sudo systemctl stop HomeHUDPi.service
$ sudo systemctl start HomeHUDPi.service
```