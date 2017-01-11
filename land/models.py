from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class LandUserProfile(models.Model):
    user = models.OneToOneField(User, )
    id_no = models.PositiveIntegerField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=13, unique=True)

    class Meta:
        verbose_name_plural = 'LandUserProfiles'

    def __unicode__(self):
        return str(self.id_no)


class Land(models.Model):
    user = models.ForeignKey(LandUserProfile, )
    title_deed = models.CharField(max_length=32, unique=True)
    map_sheet = models.CharField(max_length=32, )
    location = models.CharField(max_length=128, )
    size = models.FloatField()
    photo = models.ImageField(upload_to='land/images/')
    land_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(max_length=140)
    on_sale = models.BooleanField(default=False)
    fee_paid = models.BooleanField(default=False)
    purchased = models.BooleanField(default=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Lands'
        ordering = ('-date_registered', )

    def __unicode__(self):
        return str(self.title_deed)


class LandTransfers(models.Model):
    title_deed = models.ForeignKey(Land, related_name='LandTransfers')
    new_title_deed = models.CharField(max_length=32, unique=True)
    owner = models.ForeignKey(LandUserProfile, )
    transfer_to = models.CharField(verbose_name='Transfer To (Username)', max_length=32, )
    size_transferred = models.FloatField()
    relationship = models.CharField(max_length=64)
    date_transferred = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'LandTransfers'
        ordering = ('-date_transferred', )

    def __unicode__(self):
        return '{0} Transferred on {1}'.format(str(self.new_title_deed), str(self.date_transferred))


class LandPurchases(models.Model):
    land = models.OneToOneField(Land)
    owner = models.ForeignKey(User, )
    buyer = models.ForeignKey(LandUserProfile, )
    deposit = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=13, )
    email = models.EmailField()
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'LandPurchases'
        ordering = ('-date', )

    def __unicode__(self):
        return str(self.land)


class ContactUs(models.Model):
    first_name = models.CharField(max_length=32, )
    last_name = models.CharField(max_length=32, )
    email = models.EmailField()
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    message = models.TextField(max_length=140, )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'ContactUs Messages'
        ordering = ('-date', )

    def __unicode__(self):
        return 'message by {0} {1}'.format(self.first_name, self.last_name, )


class Notification(models.Model):
    user = models.ForeignKey(User, )
    message_from = models.CharField(max_length=32, )
    message = models.TextField(max_length=140, )
    read = models.BooleanField(default=False, )
    date = models.DateTimeField(auto_now_add=True, )

    class Meta:
        verbose_name_plural = 'Notifications'
        ordering = ('-date', )

    def __unicode__(self):
        return self.message_from