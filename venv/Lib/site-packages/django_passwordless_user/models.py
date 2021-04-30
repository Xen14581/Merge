from django.db import models
from django.utils.crypto import salted_hmac


class AbstractBaseUser(models.Model):
    last_login = models.DateTimeField(blank=True, null=True)

    is_active = True
    is_anonymous = False
    is_authenticated = True

    REQUIRED_FIELDS = []

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_username()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD,
                self.normalize_username(self.get_username()))

    def natural_key(self):
        return (self.get_username(),)

    def get_salted_hmac_key_salt(self):
        # django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return 'django_passwordless_user.models.AbstractBaseUser.get_session_auth_hash'

    def get_salted_hmac_value(self):
        return self.get_username()

    def _legacy_get_session_auth_hash(self):
        key_salt = self.get_salted_hmac_key_salt()
        value = self.get_salted_hmac_value()
        try:
            return salted_hmac(key_salt, value, algorithm='sha1').hexdigest()
        except TypeError:
            return salted_hmac(key_salt, value).hexdigest()

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = self.get_salted_hmac_key_salt()
        value = self.get_salted_hmac_value()
        try:
            return salted_hmac(key_salt, value, algorithm='sha256').hexdigest()
        except TypeError:
            return salted_hmac(key_salt, value).hexdigest()

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username
