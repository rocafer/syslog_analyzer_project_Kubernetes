from django.db import models

# Create your models here.

# analyzer/models.py

from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploaded_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class FoundError(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    error_message = models.TextField()
    line_number = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Logs(models.Model):
    ID = models.AutoField(primary_key=True)
    group_name = models.TextField()
    type = models.TextField()
    message = models.TextField()
    currdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.group_name} - {self.type} - {self.message}"
