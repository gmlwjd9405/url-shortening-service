import random
import string
import base64

from django.conf import settings

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 6)
key = 0xABCDDCBA
ID_NUM_OF_BYTES = 4 # 저장할 수 있는 url의 수는 약 42억개

# 대문자 소문자 숫자를 랜덤으로 8개를 조합하여 새로운 url을 생성하는 함수
def code_generator(size=SHORTCODE_MIN, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    new_code = ''
    for _ in range(size):
        new_code += random.choice(chars)

    return new_code


# 원래의 url에 새로운 url을 할당하는 함수
def create_shortcode(instance, size=SHORTCODE_MIN):
    new_code = code_generator(size=size)
    print("++++++instance: ", instance) # test
    print("++++++instance: ", instance.id)  # test
    instance_class = instance.__class__
    print("++++++instance_class: ", instance_class)  # test
    print("++++++instance_class: ", instance_class.id)  # test

    # 이미 존재하는 shortcode를 가지고 있다면 새로운 shortcode를 생성하여 반환
    queryset_exists = instance_class.objects.filter(shortcode=new_code).exists()
    if queryset_exists:
        return create_shortcode(instance, size=size)

    return new_code


# 원래의 url에 새로운 url을 할당하는 함수
def encode_id(instance):
    instance_class = instance.__class__
    print("++++++instance_class: ", instance_class)  # test
    print("++++++instance_class: ", instance_class.id)  # test
    id = instance_class.id
    print('id= ', id)
    # XOR을 통한 암호화
    encoded_id = (id ^ key)
    print('encoded_id= ', encoded_id)
    # 입력한 id를 byte로 변환한 후 utf-8로 decoding하여 문자열을 생성
    transferToByte = base64.b64encode(encoded_id.to_bytes(ID_NUM_OF_BYTES, byteorder='big'))
    print('transferToByte= ', transferToByte)
    encoded_str = transferToByte.decode('utf-8')
    print('encoded_str= ', encoded_str)

    # 문자열에 포함되어 있는 =는 제거하고, /와 +는 다른 것으로 대체한 shorten url을 반환
    return encoded_str.replace('=', '').replace('/', '_').replace('+', '-')


# 해당 str(shorten url)의 DB index(primary key)값을 반환하는 함수
def decode_id(str):
    # 남은 비트 수에 따라 뒤에 붙는 =의 갯수가 달라짐
    num_of_padding = 3 - ID_NUM_OF_BYTES % 3
    print('num_of_padding= ', num_of_padding)
    # 위에서 제거했던 =는 다시 붙이고, 대체했던 /와 +로 다시 되돌린다.
    str = (str + '=' * num_of_padding).replace('_', '/').replace('-', '+')
    print('str= ', str)
    # 문자열을 다시 base64로 디코딩
    decoded_id = base64.b64decode(str)
    print('decoded_id= ', decoded_id)

    # byte를 integer(primary key)로 바꾸어 반환.
    return int.from_bytes(decoded_id, byteorder='big') ^ key