# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'PomeloUser'
        db.delete_table(u'Pomelo_pomelouser')

        # Deleting model 'Gift'
        db.delete_table(u'Pomelo_gift')


    def backwards(self, orm):
        # Adding model 'PomeloUser'
        db.create_table(u'Pomelo_pomelouser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('Pomelo', ['PomeloUser'])

        # Adding model 'Gift'
        db.create_table(u'Pomelo_gift', (
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('url_video', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('receiver', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receiver', to=orm['Pomelo.PomeloUser'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sender', to=orm['Pomelo.PomeloUser'])),
        ))
        db.send_create_signal('Pomelo', ['Gift'])


    models = {
        
    }

    complete_apps = ['Pomelo']