# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'foods_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'foods', ['Category'])

        # Adding model 'Food'
        db.create_table(u'foods_food', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['foods.Category'])),
            ('heat', self.gf('django.db.models.fields.FloatField')()),
            ('carbohydrate', self.gf('django.db.models.fields.FloatField')()),
            ('fat', self.gf('django.db.models.fields.FloatField')()),
            ('protein', self.gf('django.db.models.fields.FloatField')()),
            ('cellulose', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'foods', ['Food'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'foods_category')

        # Deleting model 'Food'
        db.delete_table(u'foods_food')


    models = {
        u'foods.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'foods.food': {
            'Meta': {'object_name': 'Food'},
            'carbohydrate': ('django.db.models.fields.FloatField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['foods.Category']"}),
            'cellulose': ('django.db.models.fields.FloatField', [], {}),
            'fat': ('django.db.models.fields.FloatField', [], {}),
            'heat': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'protein': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['foods']