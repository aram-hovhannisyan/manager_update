import os
import django


# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manager.settings')
django.setup()

from account.models import User
from tables.models import ItemsModel, Global_Debt
from django.apps import apps

def clear_database():
    # Get all installed models
    all_models = apps.get_models()

    # Exclude User model and ItemsModel
    excluded_models = [User, ItemsModel, Global_Debt]

    # Iterate over models and delete records
    for model in all_models:
        if model not in excluded_models:
            model.objects.all().delete()

    print('Database cleared successfully!')


def leave_latest_global_debts():
    # Get all users
    users = User.objects.all()

    # Iterate over users and leave only the latest global debt
    for user in users:
        try:
            latest_global_debt = Global_Debt.objects.filter(customer=user).latest('timeOfCreating')
            print(user.username, latest_global_debt.debt)
            Global_Debt.objects.filter(customer=user).exclude(pk=latest_global_debt.pk).delete()
        except:
            pass
    print('Latest global debts retained successfully!')

leave_latest_global_debts()



clear_database()
