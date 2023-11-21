import requests


def send_otp_code(phone_number, code):
    data = {'from': '50004001570889', 'to': phone_number, 'text': f'  کد تایید شما{code} '}
    response = requests.post('https://console.melipayamak.com/api/send/simple/fca6e570c458459289b1366c44a25c22',
                             json=data)
    print(response.json())
