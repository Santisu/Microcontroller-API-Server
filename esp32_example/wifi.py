import network
import time

WIFI_SSID = "your_ssid"
PASSWORD = "your_password"

def connect_wifi(timeout_seconds=30):
    ssid = WIFI_SSID
    password = PASSWORD
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)

    start_time = time.time()
    
    try:
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            time.sleep(1)
            # Verifie if the timeout has been reached
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > timeout_seconds:
                break  # Returns none to indicate that the connection failed
    except OSError as e:
        print(f"Error connecting: {e}")
    return sta_if