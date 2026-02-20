# users/apps.py
from django.apps import AppConfig

# Added by Mark: This config automatically disables Django's persmission system. It needs to
# be disabled becasue migrating into MongoDB collections does not work with it.
class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from django.contrib.auth.management import create_permissions
        from django.db.models.signals import post_migrate

        post_migrate.disconnect(
            create_permissions,
            dispatch_uid="django.contrib.auth.management.create_permissions"
        )