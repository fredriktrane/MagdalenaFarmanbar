import network, time
from machine import Pin

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid = "ssid"
pw = "pwd"

wlan.connect(ssid, pw)

def light_onboard_led():
    led = machine.Pin('LED', machine.Pin.OUT)
    led.on();
    
def dark_onboard_led():
    led = machine.Pin('LED', machine.Pin.OUT)
    led.off();

timeout = 10
while timeout > 0:
    if wlan.status() >= 3:
        light_onboard_led()
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)
   
wlan_status = wlan.status()

def check_prices():
    import urequests
    import json
    url = "https://api.tibber.com/v1-beta/gql"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": "Bearer tibber_api_key",
    }
    data = {
        "query": "{ viewer { homes { currentSubscription { priceInfo { current { level, total }}}}}}"
    }
    response = urequests.post(url, headers=headers, json=data)
    response_dict = response.json()
    priceLevel = (response_dict['data']['viewer']['homes'][0]['currentSubscription']['priceInfo']['current']['level'])
    priceTotal = (response_dict['data']['viewer']['homes'][0]['currentSubscription']['priceInfo']['current']['total']) *100
    if priceLevel == 'VERY_EXPENSIVE':
        a=5
    elif priceLevel == 'EXPENSIVE':
        a=4
    elif priceLevel == 'NORMAL':
        a=3
    elif priceLevel == 'CHEAP':
        a=2
    elif priceLevel == 'VERY_CHEAP':
        a=1
    else:
        a=100
        
    if priceTotal < 30 :
        b=1
    elif priceTotal < 80 :
        b=2
    elif priceTotal < 120 :
        b=3
    elif priceTotal < 180 :
        b=4
    elif priceTotal < 250 :
        b=5
    else:
        b=100
        
    c = a+b

    print("Pricecategory: " + str(a))
    print("Pricelevel: " + str(b))
    print("Pricetotal: " + str(c))

    heater_on = False
    #if a <= 2 : # if cheap or very cheap 2
    #    heater_on_temp = True
        
    #if b <= 3 : # if price under x 3
    #    heater_on_temp = True
        
    if c <= 6 : # if price under
        heater_on = True    

    return(heater_on)

relay_low = Pin(6, Pin.OUT)
relay_high = Pin(8, Pin.OUT)

#Force run on restart
checked_prices = check_prices()
relay_low.value(checked_prices)
relay_high.value(checked_prices)

while 1:
    minute = time.localtime()[4]
    if minute == 0:
        #runcode check prices
        checked_prices = check_prices()
        relay_low.value(checked_prices)
        relay_high.value(checked_prices)
        time.sleep(60)
    else:
        time.sleep(10)
        print('Sleeping')

