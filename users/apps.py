# users/apps.py
from django.apps import AppConfig

# Added by Mark: I lowkey have no idea how this works. Will have to look into how this config works.
class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from django.contrib.auth.management import create_permissions
        from django.db.models.signals import post_migrate

        post_migrate.disconnect(
            create_permissions,
            dispatch_uid="django.contrib.auth.management.create_permissions"
        )