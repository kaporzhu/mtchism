# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserPlan'
        db.create_table(u'plans_userplan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plans.Plan'])),
            ('days', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('current_stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plans.UserStage'], null=True, blank=True)),
            ('current_days', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('status', self.gf('django.db.models.fields.CharField')(default='joined', max_length=32)),
            ('start_weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('end_weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('given_up_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('ended_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('joined_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'plans', ['UserPlan'])

        # Adding model 'UserStage'
        db.create_table(u'plans_userstage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('user_plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plans.UserPlan'])),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plans.Stage'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='ready', max_length=32)),
            ('index', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('start_weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('end_weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('current_days', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('ended_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'plans', ['UserStage'])

        # Adding model 'UserStageDay'
        db.create_table(u'plans_userstageday', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('user_stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['plans.UserStage'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'plans', ['UserStageDay'])

        # Adding M2M table for field meals on 'UserStageDay'
        m2m_table_name = db.shorten_name(u'plans_userstageday_meals')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userstageday', models.ForeignKey(orm[u'plans.userstageday'], null=False)),
            ('stagemeal', models.ForeignKey(orm[u'plans.stagemeal'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userstageday_id', 'stagemeal_id'])

        # Adding field 'Plan.is_active'
        db.add_column(u'plans_plan', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Stage.index'
        db.add_column(u'plans_stage', 'index',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'UserPlan'
        db.delete_table(u'plans_userplan')

        # Deleting model 'UserStage'
        db.delete_table(u'plans_userstage')

        # Deleting model 'UserStageDay'
        db.delete_table(u'plans_userstageday')

        # Removing M2M table for field meals on 'UserStageDay'
        db.delete_table(db.shorten_name(u'plans_userstageday_meals'))

        # Deleting field 'Plan.is_active'
        db.delete_column(u'plans_plan', 'is_active')

        # Deleting field 'Stage.index'
        db.delete_column(u'plans_stage', 'index')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'meals.dish': {
            'Meta': {'object_name': 'Dish'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'meals.meal': {
            'Meta': {'object_name': 'Meal'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['meals.MealCategory']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'dishes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['meals.Dish']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'limitations': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'price': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'meals.mealcategory': {
            'Meta': {'object_name': 'MealCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'plans.plan': {
            'Meta': {'object_name': 'Plan'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'plans.stage': {
            'Meta': {'object_name': 'Stage'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'days': ('django.db.models.fields.SmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plans.Plan']"})
        },
        u'plans.stagemeal': {
            'Meta': {'object_name': 'StageMeal'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meal': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meals.Meal']"}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plans.Stage']"})
        },
        u'plans.userplan': {
            'Meta': {'object_name': 'UserPlan'},
            'current_days': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'current_stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plans.UserStage']", 'null': 'True', 'blank': 'True'}),
            'days': ('django.db.models.fields.SmallIntegerField', [], {}),
            'end_weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'given_up_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plans.Plan']"}),
            'start_weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'joined'", 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'plans.userstage': {
            'Meta': {'object_name': 'UserStage'},
            'current_days': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'end_weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.SmallIntegerField', [], {}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plans.Stage']"}),
            'start_weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'ready'", 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'user_plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plans.UserPlan']"})
        },
        u'plans.userstageday': {
            'Meta': {'object_name': 'UserStageDay'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meals': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['plans.StageMeal']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'user_stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['plans.UserStage']"})
        }
    }

    complete_apps = ['plans']