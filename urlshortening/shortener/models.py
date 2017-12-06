from django.conf import settings
from django.db import models
# from django_hosts.resolvers import reverse
from django.core.urlresolvers import reverse
from .utils import encode_id
from .validators import validate_url

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 8)


class ShortenerURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs_main = super(ShortenerURLManager, self).all(*args, **kwargs)
        qs = qs_main.filter(active=True)
        return qs

    def refresh_shortcodes(self):
        qs = ShortenerURL.objects.filter(id__gte=1)
        new_codes = 0

        for q in qs:
            q.shortcode = encode_id(q.pk)
            q.save()
            new_codes += 1
        return "New codes made: {i}".format(i=new_codes)


class ShortenerURL(models.Model):
    url = models.CharField(max_length=220, validators=[validate_url])
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = ShortenerURLManager()

    def save(self, *args, **kwargs):
        super(ShortenerURL, self).save(*args, **kwargs)

        # shortcode가 없거나 빈 문자열인 경우 새로운 url을 할당한다
        if self.shortcode is None or self.shortcode == "":
            print('+++++++++++save q.id: ', self.pk) #test
            # DB pk를 base64로 인코딩한 shorten url을 할당한다
            self.shortcode = encode_id(self.pk)

        # 입력한 url에 http가 없으면 붙여서 저장한다
        if not "http" in self.url:
            self.url = "http://" + self.url

        super(ShortenerURL, self).save()

    def __str__(self):
        return str(self.url)

    # 뷰 함수에서 URL을 하드코딩하지 않도록
    def get_short_url(self):
        url_path = reverse("scode", kwargs={'shortcode': self.shortcode})
        url = "http://localhost:8000" + url_path
        return url
