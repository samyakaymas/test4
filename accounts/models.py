from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, username, first_name, last_name, subject, chapter, password, **extra_fields):
        values = [username, first_name, last_name, subject, chapter]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            subject=subject,
            chapter=chapter,
            is_superuser=extra_fields['is_superuser'],
            is_staff=extra_fields['is_staff'],
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, first_name, last_name, None, None, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=254,unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    subject = models.ForeignKey('theoryTag.Subject', default=None, on_delete=models.SET_NULL, blank=True, null=True)
    chapter = models.ForeignKey('theoryTag.Chapter', default=None, on_delete=models.SET_NULL, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    can_add_theory = models.BooleanField(default=True)
    can_edit_theory = models.BooleanField(default=True)
    can_see_theory = models.BooleanField(default=True)
    can_add_tag = models.BooleanField(default=True)
    can_see_tag = models.BooleanField(default=True)
    can_add_cross = models.BooleanField(default=True)
    can_see_cross = models.BooleanField(default=True)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return '{} '.format(self.first_name)