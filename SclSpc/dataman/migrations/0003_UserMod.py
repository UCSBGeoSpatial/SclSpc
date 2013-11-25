# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'dataman.category': {
            'Meta': {'object_name': 'Category'},
            'fs_id': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'pluralName': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'dataman.checkin': {
            'Meta': {'object_name': 'CheckIn'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dataman.Location']"}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dataman.Place']"}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datascrape.Service']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dataman.Tag']", 'symmetrical': 'False'}),
            'uid': ('django.db.models.fields.BigIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dataman.User']"})
        },
        u'dataman.location': {
            'Meta': {'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        u'dataman.pic': {
            'Meta': {'object_name': 'Pic'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dataman.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2400', 'null': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datascrape.Service']", 'null': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dataman.Tag']", 'null': 'True', 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'dataman.place': {
            'Meta': {'object_name': 'Place'},
            'foursq_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dataman.Category']", 'null': 'True', 'symmetrical': 'False'}),
            'foursq_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'foursq_primary_cat': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fs_prime'", 'null': 'True', 'to': u"orm['dataman.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dataman.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'venueid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'dataman.tag': {
            'Meta': {'object_name': 'Tag'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dataman.user': {
            'Meta': {'object_name': 'User'},
            'foursq_id': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'twitter_handle': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'datascrape.service': {
            'Meta': {'object_name': 'Service'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['dataman']
    symmetrical = True
