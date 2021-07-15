from __future__ import unicode_literals

from django.db import migrations


def migrate_permission(apps, schema_editor):
    Permission = apps.get_model("users", "Permission")
    module = 'products'
    manage_permissions = Permission.objects.filter(module = module)
 
    Role = apps.get_model('users', 'Role')
    roles = Role.objects.filter()
    for role in roles:
        if role.name in ['Manager']:
            role.permission.add(*manage_permissions)
        role.save()

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0005_migrate_permission')
    ]

    operations = [
        migrations.RunPython(migrate_permission),
    ]