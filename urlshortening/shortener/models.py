from django.db import models
from .utils import code_generator, create_shortcode


class ShortenerURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs_main = super(ShortenerURLManager, self).all(*args, **kwargs)
        qs = qs_main.filter(active=True)
        return qs

    def refresh_shortcodes(self, items=None):
        qs = ShortenerURL.objects.filter(id__gte=1)

        # if items is not None and isinstance(items, int):
        #     qs = qs.order_by('-id')[:items]
        # new_codes = 0

        for q in qs:
            q.shortcode = create_shortcode(q)
            print(q.id)
            q.save()
            new_codes += 1
        return "New codes made: {i}".format(i=new_codes)


class ShortenerURL(models.Model):
    url = models.CharField(max_length=220, )
    shortcode = models.CharField(max_length=8, unique=True, blank=True)
    #shortcode = models.CharField(max_length=8, null=False, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = ShortenerURLManager()

    def save(self, *args, **kwargs):
        # shortcode가 없거나 빈 문자열인 경우 새로운 url을 할당한다
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)

        super(ShortenerURL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)
