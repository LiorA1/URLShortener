
from django.urls import path
from .views import CreateViewShortener, RedirectViewUrl, create_url_mapper, RedirectViewUrl2, LastUrls, LastUrls2
from django.views.generic import TemplateView

app_name = "urlshorten"
urlpatterns = [
    path('create/', CreateViewShortener.as_view(), name="url_create"),
    path('create2/', create_url_mapper, name="url_create2"),
    path('s/<str:pk>/', RedirectViewUrl.as_view(), name="url_redirect"),
    path('s2/<str:pk>/', RedirectViewUrl2.as_view(), name="url_redirect2"),
    path('data/urls/', LastUrls2.as_view(), name="data_urls"),
    path('', TemplateView.as_view(template_name='index.html'))
]
