from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('7A5553445A757A596A784E4C6A6E6F51304A546147546971673136576D475461537071506D68776B6A51773D')
        params = {
            'sender': '',#optional
            'receptor': phone_number,#multiple mobile number, split by comma
            'message': f'کد تایید شما: {code} ',
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)