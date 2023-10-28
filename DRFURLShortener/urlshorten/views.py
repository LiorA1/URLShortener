from rest_framework import status
from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from rest_framework.response import Response
from django.urls import reverse
from urlshorten.models import UrlMapper
from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .utils import _generate_rand_str
from rest_framework import generics


from urlshorten.serializers import (
    UrlMapperSerializer,
    UrlMapperSerializerRead,
)


@api_view(["GET", "POST"])
def create_url_mapper(request):
    if request.method == "GET":
        serializer = UrlMapperSerializer()
        return Response(serializer.data)
    elif request.method == "POST":
        # Take the url from the user, generate a hash, call get_or_create
        req_data = request.data | {
            "short_path": _generate_rand_str(full_url=request.data.get("url", ""))
        }
        serializer = UrlMapperSerializer(data=req_data)

        if serializer.is_valid(raise_exception=False):
            # is_valid will fail, if there is an instance with the same short_path.
            serializer.save()  # call the serializer.create at the end.
            redirect_path = reverse(
                "urlshorten:url_redirect", args={serializer.data["short_path"]}
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


# TODO: a view that returns a list of the most 10 urls that was hit & their click counter.


class LastUrls(APIView):
    """ """

    def get(self, request, format=None):
        query = UrlMapper.objects.order_by("-hits").values("url", "hits")[:10]
        return Response(query)


class LastUrls2(generics.ListAPIView):
    queryset = UrlMapper.objects.order_by("-hits").values("url", "hits")[:10]
    serializer_class = UrlMapperSerializerRead
