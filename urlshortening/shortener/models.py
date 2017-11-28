from django.db import models
import random
import string


def code_generator(size=8, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    new_code = ''
    for _ in range(size):
        new_code += random.choice(chars)

    return new_code


class ShortenerURL(models.Model):
    url = models.CharField(max_length=220, )
    shortcode = models.CharField(max_length=8, unique=True)
    #shortcode = models.CharField(max_length=8, null=False, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.shortcode = code_generator()
        super(ShortenerURL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)
