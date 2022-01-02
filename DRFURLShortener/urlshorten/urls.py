
from django.urls import path
from .views import CreateViewShortener, RedirectViewUrl

app_name = "urlshorten"
urlpatterns = [
    path('create/', CreateViewShortener.as_view(), name="url_create"),
    path('s/<str:pk>/', RedirectViewUrl.as_view(), name="url_redirect"),
]
