# Generated by Django 5.1 on 2024-08-14 14:46

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('PENDING', 'Pending'), ('PAID', 'Paid')], default='PENDING', max_length=24, null=True)),
                ('payment_type', models.CharField(blank=True, choices=[('PAYMENT', 'Payment'), ('FINE', 'Fine')], default='PAYMENT', max_length=24, null=True)),
                ('session_url', models.URLField(blank=True, null=True)),
                ('session_id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True)),
                ('money_to_pay', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
            options={
                'ordering': ['-status'],
            },
        ),
    ]
