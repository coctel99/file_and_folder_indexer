from django.urls import path

from file_and_folder_indexer.apps.file_reader import views

filesystem_urlpatterns = [
    path('<path:url_path>/', views.filesystem_view),
]
