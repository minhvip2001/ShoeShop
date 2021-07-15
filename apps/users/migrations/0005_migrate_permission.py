from __future__ import unicode_literals

from django.db import migrations


def migrate_permission(apps, schema_editor):
    Permission = apps.get_model("users", "Permission")
    module = 'products'
    actions = ['retrieve', 'list', 'update', 'partial_update', 'delete', 'create']
    action_sale = ['retrieve', 'list']
    created_permissions = []
    for action in actions:
        created_permissions.append(Permission(
            module = module,
            action = action
        ))
    Permission.objects.bulk_create(created_permissions)

    manage_permissions = Permission.objects.filter(module = module)
    sale_permissions = Permission.objects.filter(module = module, action__in = action_sale)

    Role = apps.get_model('users', 'Role')
    roles = Role.objects.filter()
    for role in roles:
        if role.name in ['Manager']:
            role.permission.add(*manage_permissions)
        if role.name in ['Sale']:
            role.permission.add(*sale_permissions)
        role.save()

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_migrate_permission')
    ]

    operations = [
        migrations.RunPython(migrate_permission),
    ]