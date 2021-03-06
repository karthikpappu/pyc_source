# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/phoetrymaster/Development/CSAR/drf-chunked-upload/drf_chunked_upload/models.py
# Compiled at: 2017-02-26 16:48:39
# Size of source mod 2**32: 4434 bytes
import time, os.path, hashlib, uuid
from django.db import models
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.utils import timezone
from .settings import EXPIRATION_DELTA, UPLOAD_PATH, STORAGE, ABSTRACT_MODEL, COMPLETE_EXT, INCOMPLETE_EXT
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

def generate_filename(instance, filename):
    filename = os.path.join(instance.upload_dir, str(instance.id) + INCOMPLETE_EXT)
    return time.strftime(filename)


class ChunkedUpload(models.Model):
    upload_dir = UPLOAD_PATH
    UPLOADING = 1
    COMPLETE = 2
    STATUS_CHOICES = (
     (
      UPLOADING, 'Incomplete'),
     (
      COMPLETE, 'Complete'))
    id = models.UUIDField(primary_key=True, default=(uuid.uuid4), editable=False)
    file = models.FileField(max_length=255, upload_to=generate_filename,
      storage=STORAGE)
    filename = models.CharField(max_length=255)
    user = models.ForeignKey(AUTH_USER_MODEL, related_name='%(class)s',
      editable=False)
    offset = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=UPLOADING)
    completed_at = models.DateTimeField(null=True, blank=True)

    @property
    def expires_at(self):
        return self.created_at + EXPIRATION_DELTA

    @property
    def expired(self):
        return self.expires_at <= timezone.now()

    @property
    def md5(self, rehash=False):
        if getattr(self, '_md5', None) is None or rehash is True:
            md5 = hashlib.md5()
            self.close_file()
            self.file.open(mode='rb')
            for chunk in self.file.chunks():
                md5.update(chunk)
                self._md5 = md5.hexdigest()

            self.close_file()
        return self._md5

    def delete(self, delete_file=True, *args, **kwargs):
        if self.file:
            storage, path = self.file.storage, self.file.path
        (super(ChunkedUpload, self).delete)(*args, **kwargs)
        if self.file:
            if delete_file:
                storage.delete(path)

    def __unicode__(self):
        return '<%s - upload_id: %s - bytes: %s - status: %s>' % (
         self.filename, self.id, self.offset, self.status)

    def close_file(self):
        """
        Bug in django 1.4: FieldFile `close` method is not reaching all the
        way to the actual python file.
        Fix: we had to loop all inner files and close them manually.
        """
        file_ = self.file
        while file_ is not None:
            file_.close()
            file_ = getattr(file_, 'file', None)

    def append_chunk(self, chunk, chunk_size=None, save=True):
        self.close_file()
        self.file.open(mode='ab')
        self.file.write(chunk.read())
        if chunk_size is not None:
            self.offset += chunk_size
        else:
            if hasattr(chunk, 'size'):
                self.offset += chunk.size
            else:
                self.offset = self.file.size
        self._md5 = None
        if save:
            self.save()
        self.close_file()

    def get_uploaded_file(self):
        self.close_file()
        self.file.open(mode='rb')
        return UploadedFile(file=(self.file), name=(self.filename), size=(self.offset))

    def completed(self, completed_at=timezone.now(), ext=COMPLETE_EXT):
        if ext != INCOMPLETE_EXT:
            try:
                os.rename(self.file.path, os.path.splitext(self.file.path)[0] + ext)
            except OSError:
                pass
            else:
                self.file.name = os.splitext(self.file.name)[0] + ext
        self.status = self.COMPLETE
        self.completed_at = completed_at
        self.save()

    class Meta:
        abstract = ABSTRACT_MODEL