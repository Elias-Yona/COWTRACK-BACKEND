from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Customer


@receiver(pre_delete, sender=Customer)
def delete_user_with_customer(sender, instance, **kwargs):
    user = instance.user
    print(user)
    pre_delete.disconnect(delete_user_with_customer, sender=Customer)
    user.delete()
    pre_delete.connect(delete_user_with_customer, sender=Customer)
