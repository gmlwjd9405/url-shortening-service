from django.db import models
from .utils import code_generator, create_shortcode


class ShortenerURL(models.Model):
    url = models.CharField(max_length=220, )
    shortcode = models.CharField(max_length=8, unique=True, blank=True)
    #shortcode = models.CharField(max_length=8, null=False, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # shortcode가 없거나 빈 문자열인 경우 새로운 url을 할당한다
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)

        super(ShortenerURL, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.url)
