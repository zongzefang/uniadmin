from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from mptt.models import MPTTModel, TreeForeignKey


def upload_to(instance, filename):
    return 'uploads/{}/{}/avatars/{}'.format(instance.__class__.__name__, instance.id, filename)

class Label(MPTTModel):
    '''
    one of the core traits
    '''
    name_ch=models.CharField(max_length=10, unique=True)
    name_en=models.CharField(max_length=30, unique=True)
    description_ch=models.TextField(blank=True, null=True)
    description_en=models.TextField(blank=True, null=True)
    avatar=ThumbnailerImageField(blank=True, null=True, upload_to=upload_to)
    parent=TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by=['name_ch']

class TitleLabel(models.Model):
    name_ch=models.CharField(max_length=10)
    name_en=models.CharField(max_length=10)

class University(models.Model):
    '''
    for future convenience, should consider saving a map
    '''
    name_ch=models.CharField(max_length=10)
    name_en=models.CharField(max_length=30)
    email_suffix=models.CharField(max_length=20)


