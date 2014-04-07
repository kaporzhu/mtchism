# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'buildings_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal(u'buildings', ['Tag'])

        # Adding model 'Building'
        db.create_table(u'buildings_building', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('tips', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'buildings', ['Building'])

        # Adding M2M table for field tags on 'Building'
        m2m_table_name = db.shorten_name(u'buildings_building_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('building', models.ForeignKey(orm[u'buildings.building'], null=False)),
            ('tag', models.ForeignKey(orm[u'buildings.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['building_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'buildings_tag')

        # Deleting model 'Building'
        db.delete_table(u'buildings_building')

        # Removing M2M table for field tags on 'Building'
        db.delete_table(db.shorten_name(u'buildings_building_tags'))


    models = {
        u'buildings.building': {
            'Meta': {'object_name': 'Building'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['buildings.Tag']", 'symmetrical': 'False'}),
            'tips': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'buildings.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['buildings']