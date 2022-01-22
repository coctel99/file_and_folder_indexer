from django.apps import AppConfig


class FileReaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'file_and_folder_indexer.apps.file_reader'
    # allowed_file_extensions = [".txt", ".md", ".docx", ""]
    allowed_file_extensions = [".txt"]
