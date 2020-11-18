from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

import json


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Record(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    is_important = models.BooleanField(default=False)
    content = models.FileField(upload_to="content/%Y/%m/%d/", blank=True, null=True)

    class Meta:
        ordering = ("-edit_date",)
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __str__(self):
        return f'Record {self.id}'

    @property
    def children_dict(self):
        children = {}
        for child in self.children.all():
            children[child.name] = child.id
        return children

    @property
    def children_list(self):
        children = []
        for child in self.children.all():
            children.append(child.id)
        return children

    @children_list.setter
    def children_list(self, ids_list):
        assert (type(ids_list) is list), \
            (f"Expected list, got {type(ids_list)}")
        self.children.clear()
        for id in ids_list:
            record_type = RecordType.objects.filter(id=id)
            if record_type.exists():
                self.children.add(record_type[0])


class RecordType(models.Model):
    name = models.CharField(max_length=100)
    entity = models.JSONField()
    records = models.ManyToManyField(Record, related_name='children', blank=True)
    parents = models.ManyToManyField('AbstractRecordType', related_name='children')

    class Meta:
        verbose_name = 'RecordType'
        verbose_name_plural = 'RecordTypes'

    def __str__(self):
        return self.name

    @property
    def entity_as_dict(self):
        return {self.name: json.loads(self.entity)}

    @property
    def parents_list(self):
        parents = []
        for parent in self.parents.all():
            parents.append(parent.id)
        return parents


class AbstractRecordType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    entity = models.JSONField()

    class Meta:
        verbose_name = 'Abstract Record Type'
        verbose_name_plural = 'Abstract Record Types'
