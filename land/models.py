from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class LandUserProfile(models.Model):
    user = models.OneToOneField(User, )
    id_no = models.PositiveIntegerField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=13, unique=True)

    def __unicode__(self):
        return str(self.id_no)


class Land(models.Model):
    user = models.ForeignKey(LandUserProfile, )
    title_deed = models.CharField(max_length=32, unique=True)
    location = models.CharField(max_length=128, )
    size = models.FloatField()
    photo = models.ImageField(upload_to='land/images/')
    description = models.TextField(max_length=140)
    on_sale = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.title_deed)


class LandTransfers(models.Model):
    title_deed = models.ForeignKey(Land, related_name='LandTransfers')
    new_title_deed = models.CharField(max_length=32, )
    owner = models.ForeignKey(LandUserProfile, )
    transferred_to = models.ForeignKey(LandUserProfile, related_name='TransferredTo')
    size_transferred = models.FloatField()
    relationship = models.CharField(max_length=64)
    date_transferred = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return '{0} Transferred on {1}'.format(str(self.new_title_deed), str(self.date_transferred))


# class LandPurchases(models.Model):
#     title_deed = models.CharField(max_length=128, )