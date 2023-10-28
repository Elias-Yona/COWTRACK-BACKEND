from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Customer, Manager


@receiver(pre_delete, sender=Customer)
def delete_user_with_customer(sender, instance, **kwargs):
    user = instance.user
    pre_delete.disconnect(delete_user_with_customer, sender=Customer)
    user.delete()
    pre_delete.connect(delete_user_with_customer, sender=Customer)


@receiver(pre_delete, sender=Manager)
def delete_user_with_manager(sender, instance, **kwargs):
    user = instance.user
    pre_delete.disconnect(delete_user_with_manager, sender=Manager)
    user.delete()
    pre_delete.connect(delete_user_with_manager, sender=Manager)
