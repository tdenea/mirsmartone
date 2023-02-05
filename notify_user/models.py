from django.db import models
from decimal import Decimal as D
from oscar.core.loading import get_model
from oscar.apps.partner import strategy
from user.models import User

Basket = get_model('basket', 'Basket')

# Create your models here.
class AbandonedCartMailHistory(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='customer')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    first_reminder_mail_date = models.DateTimeField(null=True,blank=True)
    second_reminder_mail_date = models.DateTimeField(null=True, blank=True)
    third_reminder_mail_date = models.DateTimeField(null=True, blank=True)
    product_history = models.CharField(max_length=10000,null=True,blank=True)
    history_status = models.CharField(max_length=100)
    update_time = models.DateTimeField(auto_now_add=True)

    def total_basket(self):
        b = self.basket
        b.strategy = strategy.Default()
        return b.total_incl_tax_excl_discounts

