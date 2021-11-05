# Generated by Django 3.2.9 on 2021-11-05 12:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_inet.models


class Migration(migrations.Migration):

    dependencies = [
        ('peeringdb_server', '0079_org_add_flag'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecurityKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Security key name', max_length=255, null=True)),
                ('credential_id', models.CharField(db_index=True, max_length=255, unique=True)),
                ('credetnial_public_key', models.CharField(max_length=255, unique=True)),
                ('sign_count', models.PositiveIntegerField(default=0)),
                ('type', models.CharField(max_length=64)),
                ('passwordless_login', models.BooleanField(default=False, help_text='User has enabled this key for passwordless login')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webauthn_security_keys', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'U2F Device',
                'verbose_name_plural': 'U2F Devices',
                'db_table': 'peeringdb_webauthn_security_key',
            },
        ),
        migrations.CreateModel(
            name='UserHandle',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='webauthn_user_handle', serialize=False, to='peeringdb_server.user')),
                ('handle', models.CharField(blank=True, db_index=True, help_text='Unqiue user handle to be used to map users to their Webauthn credentials, only set if user has registered one or more security keys. Will be unique random 64 bytes', max_length=64, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Webauthn User Handle',
                'verbose_name_plural': 'Webauthn User Handles',
                'db_table': 'peeringdb_webauthn_user_handle',
            },
        ),
        migrations.AlterField(
            model_name='ixfmemberdata',
            name='asn',
            field=django_inet.models.ASNField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0)], verbose_name='ASN'),
        ),
        migrations.AlterField(
            model_name='ixlan',
            name='rs_asn',
            field=django_inet.models.ASNField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0)], verbose_name='Route Server ASN'),
        ),
        migrations.AlterField(
            model_name='network',
            name='asn',
            field=django_inet.models.ASNField(unique=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0)], verbose_name='ASN'),
        ),
        migrations.AlterField(
            model_name='networkfacility',
            name='local_asn',
            field=django_inet.models.ASNField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0)], verbose_name='Local ASN'),
        ),
        migrations.AlterField(
            model_name='networkixlan',
            name='asn',
            field=django_inet.models.ASNField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0)], verbose_name='ASN'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='flagged',
            field=models.BooleanField(blank=True, help_text='Flag the organization for deletion', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='flagged_date',
            field=models.DateTimeField(blank=True, help_text='Date when the organization was flagged', null=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=models.FileField(blank=True, help_text='Allows you to upload and set a logo image file for this organization', null=True, upload_to='logos_user_supplied/'),
        ),
        migrations.AlterField(
            model_name='userorgaffiliationrequest',
            name='asn',
            field=django_inet.models.ASNField(blank=True, help_text='The ASN entered by the user', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.CreateModel(
            name='SecurityKeyDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The human-readable name of this device.', max_length=64)),
                ('confirmed', models.BooleanField(default=True, help_text='Is this device ready for use?')),
                ('token', models.CharField(blank=True, max_length=16, null=True)),
                ('valid_until', models.DateTimeField(default=django.utils.timezone.now, help_text='The timestamp of the moment of expiry of the saved token.')),
                ('throttling_failure_timestamp', models.DateTimeField(blank=True, default=None, help_text='A timestamp of the last failed verification attempt. Null if last attempt succeeded.', null=True)),
                ('throttling_failure_count', models.PositiveIntegerField(default=0, help_text='Number of successive failed attempts.')),
                ('key', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='twofactor_device', to='peeringdb_server.securitykey')),
                ('user', models.ForeignKey(help_text='The user that this device belongs to.', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Webauthn Security Key 2FA Device',
                'verbose_name_plural': 'Webauthn Security Key 2FA Devices',
                'db_table': 'peeringdb_webauthn_2fa_device',
            },
        ),
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenge', models.BinaryField(db_index=True, max_length=64)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('auth', 'Authentication'), ('reg', 'Registration')], max_length=4)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='webauthn_challenges', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Webauthn Challenge',
                'verbose_name_plural': 'Webauthn_Challenges',
                'db_table': 'peeringdb_webauthn_challenge',
            },
        ),
    ]
