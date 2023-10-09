
from django.urls import path
from .views import RedirectViewUrl, create_url_mapper, LastUrls, LastUrls2
from django.views.generic import TemplateView

app_name = "urlshorten"
urlpatterns = [
    path('create2/', create_url_mapper, name="url_create"),
    path('s2/<str:pk>/', RedirectViewUrl.as_view(), name="url_redirect"),
    path('data/urls/', LastUrls2.as_view(), name="data_urls"),
    path('', TemplateView.as_view(template_name='index.html'))
]
