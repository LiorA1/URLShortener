

from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView
from rest_framework.response import Response
from django.urls import reverse
from urlshorten.models import UrlMapper
# Create your views here.
from rest_framework.generics import CreateAPIView

from urlshorten.serializers import UrlMapperSerializer


class CreateViewShortener(CreateAPIView):
    queryset = UrlMapper.objects.all()
    serializer_class = UrlMapperSerializer

    def perform_create(self, serializer):
        self.obj = serializer.save()

    def create(self, request, *args, **kwargs):
        # Handle the un-successful responses.
        response = super().create(request, *args, **kwargs)

        redirect_path = reverse("urlshorten:url_redirect", args={self.obj.short_path_creation})

        return Response({
            'status_code': 201,
            'short_url': request.build_absolute_uri(redirect_path)
        })


class RedirectViewUrl(RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        """
        Handle the redirect url lookup using UrlMapper.
        It also manage the hits counter, because the redirect-url, returned by it.
        """

        url_mapper = get_object_or_404(UrlMapper, short_path=kwargs['pk'])

        url_mapper.increase_hits() 
        # permanent is True so the browser will cache the redirect.

        return url_mapper.url
