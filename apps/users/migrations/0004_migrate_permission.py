from __future__ import unicode_literals

from django.db import migrations


def migrate_permission(apps, schema_editor):
    Permission = apps.get_model("users", "Permission")
    module = 'users'
    actions = ['retrieve', 'list', 'update', 'partial_update']
    created_permissions = []
    for action in actions:
        created_permissions.append(Permission(
            module = module,
            action = action
        ))
    Permission.objects.bulk_create(created_permissions)

    Role = apps.get_model('users', 'Role')
    roles = Role.objects.filter()
    permissions = Permission.objects.filter(module = module)
    for role in roles:
        if role.name in ['Admin']:
            role.permission.add(*permissions)
        role.save()

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_auto_20210712_1552')
    ]

    operations = [
        migrations.RunPython(migrate_permission),
    ]
