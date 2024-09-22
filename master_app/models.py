from django.db import models
import uuid

# from datetime import timedelta



# Create your models here.


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    short_url = models.CharField(max_length=300, blank=True)
    long_url = models.URLField("Long URL", blank=True, default="")
    token = models.CharField("Document Token", blank=True, default="", max_length=12)
    file_hash = models.CharField("SHA1 Hashsum", blank=True, default="", max_length=50)
    uploaded_at = models.DateTimeField("Created at",auto_now_add=True)
    expires_at = models.DateTimeField("Expires at",auto_now_add=True, blank=True, null=True)
    file_type = models.CharField("File Content Type", blank=True, default="", max_length=20)
    file_size = models.CharField("File Size (in bytes)", blank=True, default="", max_length=20)
    destroyAfterDownload = models.BooleanField("Destroy File After Download", blank=True, default=False)
    valid_link = models.BooleanField("Valid Link To Access", blank=True, default=True)
    user_agent = models.CharField("User-Agent ", blank=True, default="", max_length=500)
    ip_address = models.CharField("IP Address ", blank=True, default="", max_length=20)
    random_filename = models.BooleanField("Random Filename", blank=True, default=True)
    enable_shorturl = models.BooleanField("Enable Short Url", blank=True, default=True)
    

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return "{}".format(self.name)
    

class DocumentLogs(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField("Document Log Timestamp",auto_now_add=True)
    public_ip_address = models.CharField("User Public IP Address", blank=True, default="", max_length=50)
    user_agent = models.CharField("User-Agent", blank=True, default="", max_length=255)
    
    def __str__(self):
        return self.public_ip_address
    

class UserLogs(models.Model):
    timestamp = models.DateTimeField("Log Timestamp",auto_now_add=True)
    public_ip_address = models.CharField("User Public IP Address", blank=True, default="", max_length=50)
    user_agent = models.CharField("User-Agent", blank=True, default="", max_length=255)
    
    def __str__(self):
        return self.public_ip_address
    
class AdminLogs(models.Model):
    timestamp = models.DateTimeField("Log Timestamp",auto_now_add=True)
    public_ip_address = models.CharField("User Public IP Address", blank=True, default="", max_length=50)
    user_agent = models.CharField("User-Agent", blank=True, default="", max_length=255)
    
    def __str__(self):
        return self.public_ip_address
    

class Reports(models.Model):
    url = models.URLField("Reporting URL", max_length=250)
    email  = models.EmailField("Reporter Email Address" , max_length=50, blank=True)
    comments = models.TextField("Comments", blank=True)

    def __str__(self):
        return f"{self.url} - {self.email}"