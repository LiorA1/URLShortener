
from datetime import datetime, timedelta
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
            'status': 201,
            'short_url': request.build_absolute_uri(redirect_path)
        })


class RedirectViewUrl(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        """
        Handle the redirect url lookup using UrlMapper.
        It also manage the hits counter, because the redirect-url, returned by it.
        """

        url_mapper = get_object_or_404(UrlMapper, short_path=kwargs['pk'])

        # For each session and short url item - store a "last_visitied" value (in str).
        # If the current session visited the specific url in the last 24 hr - it will not increase the object hits counter.
        datetime_now = datetime.now()
        last_visited_key = f"last_visited_{kwargs['pk']}"
        last_visited_str = self.request.session.get(last_visited_key, None)
        last_visited_datetime = None if last_visited_str is None else datetime.fromisoformat(last_visited_str)

        if last_visited_datetime is None or (last_visited_datetime < datetime_now - timedelta(hours=24)):
            url_mapper.increase_hits()

        date_time_now_str = datetime.isoformat(datetime_now)
        self.request.session[last_visited_key] = date_time_now_str

        return url_mapper.url
