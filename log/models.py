from django.db import models


class Log(models.Model):
    type = models.CharField(max_length=100, null=True)
    view = models.TextField(null=True)
    request = models.TextField(null=True)
    body = models.TextField(null=True)
    log = models.TextField(null=True)
    device = models.TextField(null=True)
    ip = models.CharField(max_length=15, null=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.type} - {self.view} - {self.log[:20]}'
