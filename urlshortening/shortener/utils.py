import random
import string
import base64

# from django.conf import settings

# SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 6)
key = 0xABCDDCBA # 임의로 지정
ID_NUM_OF_BYTES = 4 # 저장할 수 있는 url의 수는 약 42억개


# 원래의 long url의 DB primary key를 이용하여 새로운 short url을 할당하는 함수
def encode_id(id):
    # XOR을 통한 암호화
    encoded_id = (id ^ key)
    print('encoded_id= ', encoded_id)

    # 입력한 id를 byte로 변환
    transferToByte = base64.b64encode(encoded_id.to_bytes(ID_NUM_OF_BYTES, byteorder='big'))
    # byte를 utf-8로 decoding하여 문자열(short url)을 생성
    encoded_str = transferToByte.decode('utf-8')
    print('encoded_str= ', encoded_str)

    # 문자열에 포함되어 있는 =는 제거하고, /와 +는 다른 것으로 대체한 shorten url을 반환
    return encoded_str.replace('=', '').replace('/', '_').replace('+', '-')


# 해당 str(shorten url)의 DB primary key 값을 반환하는 함수
def decode_id(str):
    # 남은 비트 수에 따라 뒤에 붙는 =의 갯수가 달라짐
    num_of_padding = 3 - ID_NUM_OF_BYTES % 3

    # 위에서 제거했던 =는 다시 붙이고, 대체했던 /와 +로 다시 되돌림
    str = (str + '=' * num_of_padding).replace('_', '/').replace('-', '+')
    # 문자열을 다시 base64로 디코딩하여 byte를 구한다
    decoded_id = base64.b64decode(str)
    print('decoded_id= ', decoded_id)

    # byte를 integer(primary key)로 바꾸어 반환
    return int.from_bytes(decoded_id, byteorder='big') ^ key