# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Food', fields ['name']
        db.create_index(u'foods_food', ['name'])


    def backwards(self, orm):
        # Removing index on 'Food', fields ['name']
        db.delete_index(u'foods_food', ['name'])


    models = {
        u'foods.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'foods.food': {
            'Meta': {'object_name': 'Food'},
            'carbohydrate': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['foods.Category']"}),
            'cellulose': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'fat': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'heat': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'origin_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'protein': ('django.db.models.fields.FloatField', [], {'default': '-1'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['foods']