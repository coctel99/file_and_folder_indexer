from django.urls import path

from file_reader import views

filepath_urlpatterns = [
    path('', views.filesystem_view),
    path('<path:url_path>/', views.filesystem_view),
]
