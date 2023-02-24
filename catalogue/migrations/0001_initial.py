# Generated by Django 4.1 on 2023-02-23 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Categories",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nom_categorie",
                    models.CharField(
                        max_length=250, verbose_name="nom de la categorie"
                    ),
                ),
                (
                    "created_at_categorie",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date creation de la categorie"
                    ),
                ),
                (
                    "date_de_publication_categorie",
                    models.DateField(
                        default="2022-11-10",
                        verbose_name="date de publication de la categorie ",
                    ),
                ),
                (
                    "image_categorie",
                    models.ImageField(
                        upload_to="categories/",
                        verbose_name="image de la categorie du modele",
                    ),
                ),
            ],
            options={"verbose_name": "categorie",},
        ),
        migrations.CreateModel(
            name="Modeles",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nom_modele",
                    models.CharField(
                        blank=True, max_length=250, verbose_name="nom modele"
                    ),
                ),
                (
                    "created_at_modele",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date creation du modele"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description du modele"),
                ),
                (
                    "date_de_publication",
                    models.DateField(
                        default="2022-11-10",
                        verbose_name="date de publication du modele ",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        upload_to="categories/", verbose_name="image du modele"
                    ),
                ),
                (
                    "categorie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalogue.categories",
                    ),
                ),
                (
                    "favourites",
                    models.ManyToManyField(
                        blank=True,
                        default=None,
                        related_name="favourite",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name": "modele",},
        ),
        migrations.CreateModel(
            name="Image_details",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "img_detail",
                    models.ImageField(
                        upload_to="categories/",
                        verbose_name="image de profile du modele",
                    ),
                ),
                (
                    "img_detail_modele",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalogue.modeles",
                    ),
                ),
            ],
            options={"verbose_name": "image detail du modele",},
        ),
        migrations.CreateModel(
            name="Favories",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "value_fav",
                    models.BooleanField(default=False, verbose_name="value_fav"),
                ),
                (
                    "modele_fav",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalogue.modeles",
                    ),
                ),
                (
                    "user_fav",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name": "favorie",},
        ),
    ]
