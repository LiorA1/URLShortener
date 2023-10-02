from rest_framework import status
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from rest_framework.response import Response
from django.urls import reverse
from urlshorten.models import UrlMapper, UrlMapper2
from django.db.models import F
from rest_framework.decorators import api_view

from .utils import _generate_rand_str


# Create your views here.
from rest_framework.generics import CreateAPIView

from urlshorten.serializers import UrlMapperSerializer, UrlMapperSerializer2, UrlMapperSerializerRead


class CreateViewShortener(CreateAPIView):
    queryset = UrlMapper.objects.all()
    serializer_class = UrlMapperSerializer

    def perform_create(self, serializer):
        # we will save it, but also associate it in 'self', so we can return the short_path.
        self.obj = serializer.save()

    def create(self, request, *args, **kwargs):
        # Handle the un-successful responses.

        # response = super().create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # try 'attempts' of times to create an object:
        attempts = 10
        while attempts:
            try:
                self.perform_create(serializer)
            except Exception as e:
                print(f"The exception was:\n{e}")
                if attempts == 0:
                    raise e
            finally:
                attempts = attempts - 1

        print(f"serializer.data is:{serializer.data}")

        headers = self.get_success_headers(serializer.data)

        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        redirect_path = reverse("urlshorten:url_redirect", args={self.obj.short_path})
        return Response(
            {
                "status_code": status.HTTP_201_CREATED,
                "short_url": request.build_absolute_uri(redirect_path),
            },
            headers=headers,
        )


@api_view(["GET", "POST"])
def create_url_mapper(request):
    if request.method == "GET":
        serializer = UrlMapperSerializer2()
        return Response(serializer.data)
    elif request.method == "POST":
        # Take the url from the user, generate a hash, call get_or_create
        req_data = request.data | {"short_path": _generate_rand_str(full_url=request.data.get('url', ""))}
        serializer = UrlMapperSerializer2(data=req_data)
        
        if serializer.is_valid(raise_exception=False):
            # is_valid will fail, if there is an instance with the same short_path.
            serializer.save()  # call the serializer.create at the end.
            redirect_path = reverse(
                "urlshorten:url_redirect2", args={serializer.data["short_path"]}
            )
            res_data = {
                "short_url": request.build_absolute_uri(redirect_path),
            }
            return Response(data=res_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectViewUrl(RedirectView):
    permanent = True  # returns http 301 response.

    def get_redirect_url(self, *args, **kwargs):
        """
        Handle the redirect url lookup using UrlMapper.
        It also manage the hits counter, because the redirect-url, returned by it.
        """

        url_mapper = UrlMapper.objects.filter(short_path=kwargs["pk"]).update(
            hits=F("hits") + 1
        )
        url_mapper = get_object_or_404(UrlMapper, short_path=kwargs["pk"])
        # permanent is True so the browser will cache the redirect.

        return url_mapper.url


class RedirectViewUrl2(RedirectView):
    permanent = True  # returns http 301 response.

    def get_redirect_url(self, *args, **kwargs):
        """
        Handle the redirect url lookup using UrlMapper.
        It also manage the hits counter, because the redirect-url, returned by it.
        """

        url_mapper = UrlMapper2.objects.filter(short_path=kwargs["pk"]).update(
            hits=F("hits") + 1
        )
        url_mapper = get_object_or_404(UrlMapper2, short_path=kwargs["pk"])
        # permanent is True so the browser will cache the redirect.

        return url_mapper.url


# TODO: a view that returns a list of the latest 10 urls that was clicked & their click counter.

# UrlMapper2.objects.order_by("-hits").values()[:10]
from rest_framework.views import APIView

class LastUrls(APIView):
    """
    """

    def get(self, request, format=None):
        query = UrlMapper2.objects.order_by("-hits").values("url", "hits")[:10]
        return Response(query)

from rest_framework import generics

class LastUrls2(generics.ListAPIView):
    queryset = UrlMapper2.objects.order_by("-hits").values("url", "hits")[:10]
    serializer_class = UrlMapperSerializerRead