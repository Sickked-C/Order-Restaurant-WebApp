# Generated by Django 5.2 on 2025-04-23 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_remove_order_table_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.CharField(choices=[('mi', 'Mì'), ('com', 'Cơm'), ('nuoc', 'Nước uống'), ('nuoc_tra_sua', 'Trà sữa'), ('nuoc_tra', 'Trà'), ('nuoc_topping', 'Topping'), ('nuoc_khac', 'Các loại khác'), ('anvat', 'Ăn vặt'), ('mon_them', 'Món thêm')], default='mi', max_length=20, verbose_name='Thể loại'),
        ),
    ]
