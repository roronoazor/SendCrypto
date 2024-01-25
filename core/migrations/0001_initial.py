# Generated by Django 4.1.7 on 2024-01-24 21:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("failed", "Failed"),
                            ("pending", "Pending"),
                            ("success", "Success"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
                ("source", models.CharField(max_length=255, null=True)),
                ("currency", models.CharField(max_length=100, null=True)),
                ("invoice_id", models.CharField(max_length=255, null=True)),
                ("amount", models.CharField(max_length=1000, null=True)),
                ("payload", models.JSONField(default=dict, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=2000)),
                ("phone", models.CharField(max_length=20)),
                ("country", models.CharField(max_length=20)),
                ("currency", models.CharField(max_length=3)),
                ("annual_income", models.CharField(max_length=100)),
                ("referral", models.CharField(max_length=100)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]