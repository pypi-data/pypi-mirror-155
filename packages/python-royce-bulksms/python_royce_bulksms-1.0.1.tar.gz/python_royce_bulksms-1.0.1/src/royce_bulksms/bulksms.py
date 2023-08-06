import requests

def sendSMS(phone_number,message,sender_id,api_key):
    # 74|r816nf9OSVy5qwQ3unPKel0i7SIflSFNMFk2TDKz
    endpoint = "https://bulksms.roycetechnologies.co.ke/api/sendmessage"
    data ={
    'sender_id': sender_id, 'text_message': message, 'phone_number': phone_number
    }

    headers = {
    "Authorization": "Bearer "+api_key
    }

    response=requests.post(endpoint, data=data, headers=headers)

    return response.json()

def deliveryReport(message_id,api_key):
    endpoint = "https://bulksms.roycetechnologies.co.ke/api/delivery-report"
    data ={
    'message_id': message_id
    }

    headers = {
    "Authorization": "Bearer "+api_key
    }

    response=requests.post(endpoint, data=data, headers=headers)

    return response.json()




    