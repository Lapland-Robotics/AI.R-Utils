# Wi-Fi Connector

This Python program provides a simple web interface for managing WiFi connections. It allows scanning for available WiFi networks, connecting to a specific network, checking the current connection status.
This startup program of the main system(brain) of the ATV/Robot start.

## Installation

To use this Flask REST API, ensure you have Python3 installed on your system and pip for python3. You can install Flask and its dependencies using pip:

```bash
pip install flask
```

## Cron Job 

Copy the python file to /bin:
```
sudo cp -i /path/to/repo/wifi-connector/wifi-connector.py /bin
```
Add A New Cron Job:
```
sudo crontab -e
```
Scroll to the bottom and add the following line (after all the #'s):
```
@reboot python3 /bin/wifi-connector.py 2>&1 tee /path/to/wifi-connector.log &
```
The “&” at the end of the line means the command is run in the background and it won’t stop the system booting up.


## Endpoints

#### 1. Get WiFi Connection Status

- **path:** `/status`
- **Description:** Retrieves the current WiFi connection status.
- **Request:** 
  - Method: GET
- **Response:** 
  - Status Code: 200 (OK)
  - Content Type: application/json
  - Body:
    ```json
    {
      "current_network": "Your_WiFi_SSID",
      "ip_address": "192.168.1.100"
    }
    ```


#### 2. Connect to WiFi Network

- **URL:** `/connect`
- **Description:** Connects to a specified WiFi network.
- **Request:** 
  - Method: POST
  - Content Type: application/json
  - Body:
    ```json
    {
      "ssid": "Your_WiFi_SSID",
      "password": "Your_WiFi_Password"
    }
    ```
- **Response:** 
  - Status Code: 200 (OK)
  - Content Type: application/json
  - Body:
    ```json
    {
      "message": "Connected to Your_WiFi_SSID"
    }
    ```

#### 3. Scan Available WiFi Networks

- **URL:** `/scan`
- **Description:** Retrieves a list of available WiFi networks.
- **Request:** 
  - Method: GET
- **Response:** 
  - Status Code: 200 (OK)
  - Content Type: application/json
  - Body:
    ```json
    {
      "available_networks": [
        {
          "BSSID": "270",
          "MODE": "Mbit/s  74      ▂▄▆_  WPA2",
          "SSID": "*       00:40:FF:0F:72:C9  LR54-5G-mustaboxi    Infra"
        },
        {
          "BSSID": "260",
          "MODE": "Mbit/s  69      ▂▄▆_  WPA2 802.1X",
          "SSID": "CC:BB:FE:D9:15:D2  eduroam              Infra"
        }
        ...
      ]
    }
    ```
