import uuid
from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField


class TimeStampedMixin(models.Model):
    class Meta:
        abstract = True
    db_updated_at = models.DateTimeField(auto_now=True)
    db_created_at = models.DateTimeField(auto_now_add=True)


class Burrito(TimeStampedMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, db_index=True)

    url = models.TextField(db_index=True)   # original URL
    thumbnail_url = models.TextField()
    source = models.TextField()

    banner_url = models.TextField(null=True)    # banner click-thru URL
    banner_message = models.TextField()
    banner_color_scheme = JSONField()

    stage = models.TextField()
