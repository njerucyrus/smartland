from django.db import models


class LandTransferFee(models.Model):
    land_size = models.FloatField()
    fee_charged = models.FloatField()

    class Meta:
        verbose_name_plural = 'LandTransferFee'

    def __unicode__(self):
        return "{0} hectares @ Ksh {1} fee".format(str(self.land_size), str(self.fee_charged))


class LandTransferPayment(models.Model):
    transaction_id = models.CharField(max_length=128, unique=True, db_index=True)
    title_deed = models.CharField(max_length=32, )
    transferred_size = models.FloatField()
    phone_number = models.CharField(max_length=13, )
    payment_mode = models.CharField(max_length=20, )
    amount = models.FloatField()
    status = models.CharField(max_length=32, default='PendingConfirmation')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'LandTransferPayments'

    def __unicode__(self):
        return self.transaction_id


class LandPurchasePayment(models.Model):
    transaction_id = models.CharField(max_length=128, unique=True, db_index=True)
    title_deed = models.CharField(max_length=32, )
    purchased_size = models.FloatField()
    payment_mode = models.CharField(max_length=20, )
    buyer_email = models.EmailField()
    amount = models.FloatField()
    status = models.CharField(max_length=32, )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'LandPurchasePayments'

    def __unicode__(self):
        return self.transaction_id

