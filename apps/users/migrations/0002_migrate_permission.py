from __future__ import unicode_literals

from django.db import migrations


def migrate_permission(apps, schema_editor):
    Permission = apps.get_model("users", "Permission")
    Permission.objects.create(
        module='users',
        action='profile'
    )

    Role = apps.get_model('users', 'Role')
    roles = Role.objects.filter()
    permissions = Permission.objects.filter(module='users', action='profile')

    for role in roles:
        if role.name in ['Admin', 'Sale']:
            role.permission.add(*permissions)
        role.save()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial')
    ]

    operations = [
        migrations.RunPython(migrate_permission),
    ]
