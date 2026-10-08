
from django.core.files.storage import FileSystemStorage
from django.conf import settings


# create storage path

class ProtectedFileSystemStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(location=settings.PROTECTED_MEDIA_ROOT, *args, **kwargs)
