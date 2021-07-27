from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('products', '0006_auto_20210713_1737')
    ]

    operations = [
        migrations.AddField('Product', 'quantity', models.PositiveIntegerField(blank=False, null=False, default=1)),
    ]