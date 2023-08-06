# Python Bulksms package
 Integrate bulk sms into your python project in under 2 minutes

## Steps
- Install this package
- Open A free account [here](https://bulksms.roycetechnlogies.co.ke)
- Generate API key under API menu
- use our default sender ID  `RoyceLtd`

## Installation


``` 
pip install python-royce-bulksms
 ```
 Ensure that `requests` package is installed 
``` 
pip install requests
 ```

 # How to use the package

```
from bulksms import sendSMS

sendSMS(phone_number,message,sender_id,api_key)

```

## Sample response
```
{
    'message': 'Messages sent successfully', 
    'code': 1, 'status': 'Sent To Network', 
    'response_description': 'Sent To Network', 
    'message_id': '968c1d13-ef31-4e04-a46b-8b7cd0d392fa'
}

```

# Delivery Report
```
from bulksms import deliveryReport

deliveryReport(message_id,api_key)

```



## Sample Response

```
{
    'message': 'Message delivery report', 
    'code': 1, 'response_code': 1001, 
    'status': 'Message delivery report',
     'delivery_status': 'DeliveredToTerminal', 
     'delivery_tat': '5s', 
     'delivery_time': '2022-06-15 12:51:11', 
     'message_id': '968c255e-4b03-40da-9762-786793cf1cd8'
}
```

For support call +254 713 727 937 email developer@roycetechnologies.co.ke