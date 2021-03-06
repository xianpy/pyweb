# Generated by Django 2.0.6 on 2019-01-23 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foodtypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeid', models.CharField(max_length=20)),
                ('typename', models.CharField(max_length=20)),
                ('childtypenames', models.CharField(max_length=200)),
                ('typesort', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.CharField(max_length=20)),
                ('productimg', models.CharField(max_length=150)),
                ('productname', models.CharField(max_length=100)),
                ('productlongname', models.CharField(max_length=1500)),
                ('isxf', models.BooleanField()),
                ('pmdesc', models.BooleanField()),
                ('specifics', models.CharField(max_length=20)),
                ('price', models.FloatField()),
                ('marketprice', models.FloatField()),
                ('categoryid', models.IntegerField()),
                ('childcid', models.IntegerField()),
                ('childcidname', models.CharField(max_length=30)),
                ('dealerid', models.CharField(max_length=20)),
                ('storenums', models.IntegerField()),
                ('productnum', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Mainshow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trackid', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=100)),
                ('img', models.CharField(max_length=200)),
                ('categoryid', models.CharField(max_length=30)),
                ('brandname', models.CharField(max_length=30)),
                ('img1', models.CharField(max_length=200)),
                ('childcid1', models.CharField(max_length=30)),
                ('productid1', models.CharField(max_length=30)),
                ('longname1', models.CharField(max_length=50)),
                ('price1', models.FloatField()),
                ('marketprice1', models.FloatField()),
                ('img2', models.CharField(max_length=200)),
                ('childcid2', models.CharField(max_length=30)),
                ('productid2', models.CharField(max_length=30)),
                ('longname2', models.CharField(max_length=50)),
                ('price2', models.FloatField()),
                ('marketprice2', models.FloatField()),
                ('img3', models.CharField(max_length=200)),
                ('childcid3', models.CharField(max_length=30)),
                ('productid3', models.CharField(max_length=30)),
                ('longname3', models.CharField(max_length=50)),
                ('price3', models.FloatField()),
                ('marketprice3', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Mustbuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField()),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='axf.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalPrice', models.FloatField()),
                ('ordertime', models.DateTimeField(auto_now=True)),
                ('orderstate', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkman', models.CharField(max_length=30)),
                ('area', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('postal', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=11)),
                ('telephone', models.CharField(max_length=20)),
                ('remark', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=12, unique=True)),
                ('password', models.CharField(max_length=256)),
                ('tel', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=30)),
                ('icon', models.ImageField(upload_to='icons/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=100)),
                ('realname', models.CharField(max_length=100)),
                ('qq', models.IntegerField(max_length=30)),
                ('sex', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=100)),
                ('cellphone', models.CharField(max_length=20)),
                ('idcard', models.CharField(max_length=30)),
                ('area', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('marital', models.CharField(max_length=10)),
                ('income', models.CharField(max_length=30)),
                ('hobbies', models.CharField(max_length=300)),
                ('info_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='axf.User')),
            ],
        ),
        migrations.CreateModel(
            name='Wheel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='shiadd',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='axf.User'),
        ),
        migrations.AddField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='axf.User'),
        ),
        migrations.AddField(
            model_name='ordergoods',
            name='orders',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='axf.Orders'),
        ),
    ]
