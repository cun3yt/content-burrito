import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from jsonfield import JSONField
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class TimeStampedMixin(models.Model):
    class Meta:
        abstract = True
    db_updated_at = models.DateTimeField(auto_now=True)
    db_created_at = models.DateTimeField(auto_now_add=True)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'user'
        ordering = ('full_name', )

    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('first name'), max_length=40, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        full_name = '%s' % self.full_name
        return full_name.strip()

    def get_short_name(self):
        return self.full_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Burrito(TimeStampedMixin):
    class Meta:
        db_table = 'burrito'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, db_index=True)

    url = models.TextField(db_index=True)   # original URL
    thumbnail_url = models.TextField()
    source = models.TextField()

    banner_url = models.TextField(null=True)    # banner click-thru URL
    banner_message = models.TextField()
    banner_color_scheme = JSONField(default={})

    stage = models.TextField()


class BetaSubscriber(TimeStampedMixin):
    class Meta:
        db_table = 'beta_subscriber'

    email = models.EmailField(_('email address'), unique=True)
    ip = models.TextField(null=True, blank=True)
