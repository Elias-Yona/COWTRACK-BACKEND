from django.db.models.signals import pre_delete
from django.dispatch import receiver, Signal
from .models import Customer, Manager, SalesPerson, Supervisor, Supplier


supervisor_removed_from_branch = Signal()
supervisor_transferred_to_branch = Signal()


@receiver(supervisor_removed_from_branch)
def send_removed_from_branch_email(sender, **kwargs):
    print(
        f'Hello {kwargs.get("supervisor_id")} You are no longer the supervisor of branch {kwargs.get("branch_id")}')


@receiver(supervisor_transferred_to_branch)
def send_transferred_to_branch_email(sender, **kwargs):
    print(
        f'Hello {kwargs.get("supervisor_id")} You have been transferred to the branch {kwargs.get("branch_id")}')


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


@receiver(pre_delete, sender=SalesPerson)
def delete_user_with_salesperson(sender, instance, **kwargs):
    user = instance.user
    pre_delete.disconnect(delete_user_with_salesperson, sender=SalesPerson)
    user.delete()
    pre_delete.connect(delete_user_with_salesperson, sender=SalesPerson)


# @receiver(pre_delete, sender=Supervisor)
# def delete_user_with_supervisor(sender, instance, **kwargs):
#     user = instance.user
#     pre_delete.disconnect(delete_user_with_supervisor, sender=Supervisor)
#     user.delete()
#     pre_delete.connect(delete_user_with_supervisor, sender=Supervisor)


@receiver(pre_delete, sender=Supplier)
def delete_user_with_supplier(sender, instance, **kwargs):
    user = instance.user
    pre_delete.disconnect(delete_user_with_supplier, sender=Supplier)
    user.delete()
    pre_delete.connect(delete_user_with_supplier, sender=Supplier)
