from django.apps import AppConfig


class FileReaderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'file_and_folder_indexer.apps.file_reader'
    # allowed_file_extensions = [".txt", ".md", ".docx", ""]
    allowed_file_extensions = ['.txt', '.docx']
    encodings_queue = ['utf-8', 'Windows-1251', 'cp932', 'big5']
