import random
import string

from django.conf import settings


SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 8)


# 대문자 소문자 숫자를 랜덤으로 8개를 조합하여 새로운 url을 생성하는 함수
def code_generator(size=8, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    new_code = ''
    for _ in range(size):
        new_code += random.choice(chars)

    return new_code


# 원래의 url에 새로운 url을 할당하는 함수
def create_shortcode(instance, size=8):
    new_code = code_generator(size=size)
    print(instance) # test
    instance_class = instance.__class__

    # 이미 존재하는 shortcode를 가지고 있다면 새로운 shortcode를 생성하여 반환
    queryset_exists = instance_class.objects.filter(shortcode=new_code).exists()
    if queryset_exists:
        return create_shortcode(instance, size=size)

    return new_code