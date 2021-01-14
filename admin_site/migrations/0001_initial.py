
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
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_type', models.CharField(choices=[('Food', 'Food'), ('Beverages', 'Beverages'), ('Pharmaceuticals', 'Pharmaceuticals')], max_length=200, verbose_name='Category Type(English)')),
                ('category_type_am', models.CharField(choices=[('Food', 'Food'), ('Beverages', 'Beverages'), ('Pharmaceuticals', 'Pharmaceuticals')], max_length=200, verbose_name='Category Type(Amharic)')),
                ('category_name', models.CharField(max_length=200, verbose_name='Category Name(English)')),
                ('category_name_am', models.CharField(max_length=200, verbose_name='Category Name(Amharic)')),
                ('description', models.TextField(verbose_name='Description(English)')),
                ('description_am', models.TextField(verbose_name='Description(Amharic)')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Product Name(English)')),
                ('name_am', models.CharField(max_length=255, verbose_name='Product Name(Amharic)')),
                ('description', models.TextField(default='', verbose_name='Product Description(English)')),
                ('description_am', models.TextField(default='', verbose_name='Product Description(Amharic)')),
                ('image', models.ImageField(upload_to='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category_name', models.CharField(max_length=200, verbose_name='Sub-Category Name(English)')),
                ('sub_category_name_am', models.CharField(max_length=200, verbose_name='Sub-Category Name(Amharic)')),
                ('description', models.TextField(verbose_name='Description (English)')),
                ('description_am', models.TextField(verbose_name='Description (Amharic)')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('category_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_site.category', verbose_name='Category Type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('startdate', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(auto_now_add=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_site.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_site.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_site.subcategory', verbose_name='Product Category'),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
