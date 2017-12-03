from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View

from .forms import SubmitUrlForm
from .models import ShortenerURL


class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitUrlForm()
        bg_image = "../static/img/background.jpg"
        context = {
            "title": "URL Shortening Service",
            "form": the_form,
            "bg_image": bg_image
        }
        template = "shortener/home.html"
        # template = "index.html"

        return render(request, template, context)

    def post(self, request, *args, **kwargs):
        the_form = SubmitUrlForm(request.POST)

        context = {
            "title": "URL Shortening Service",
            "form": the_form,
        }
        template = "shortener/home.html"
        # template = "index.html"

        # 모든 유효성 검증 규칙을 통과했다면
        if the_form.is_valid():
            submit_url = the_form.cleaned_data.get("url")
            # 해당 url의 객체를 DB에서 가져오거나 새로 생성한다
            obj, created = ShortenerURL.objects.get_or_create(url=submit_url)
            context = {
                "object": obj,
                "created": created,
            }

            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"

        return render(request, template, context)


class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        # 입력한 short url을 이용하여 ShortenerURL query set을 가져온다
        qs = ShortenerURL.objects.filter(shortcode__iexact=shortcode)
        obj_url = None

        # 입력한 short url에 해당하는 객체가 여러 개이거나 없으면 404에러 처리
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        obj_url = obj.url

        # short url에 해당하는 원래의 긴 url로 redirect한다
        return HttpResponseRedirect(obj_url)

