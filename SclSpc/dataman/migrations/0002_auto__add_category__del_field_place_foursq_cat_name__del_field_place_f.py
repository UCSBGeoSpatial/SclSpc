# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'dataman_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('pluralName', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('shortName', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('fs_id', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'dataman', ['Category'])

        # Deleting field 'Place.foursq_cat_name'
        db.delete_column(u'dataman_place', 'foursq_cat_name')

        # Deleting field 'Place.foursq_cat_id'
        db.delete_column(u'dataman_place', 'foursq_cat_id')

        # Adding field 'Place.foursq_primary_cat'
        db.add_column(u'dataman_place', 'foursq_primary_cat',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='fs_prime', null=True, to=orm['dataman.Category']),
                      keep_default=False)

        # Adding M2M table for field foursq_categories on 'Place'
        m2m_table_name = db.shorten_name(u'dataman_place_foursq_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('place', models.ForeignKey(orm[u'dataman.place'], null=False)),
            ('category', models.ForeignKey(orm[u'dataman.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['place_id', 'category_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'dataman_category')

        # Adding field 'Place.foursq_cat_name'
        db.add_column(u'dataman_place', 'foursq_cat_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'Place.foursq_cat_id'
        db.add_column(u'dataman_place', 'foursq_cat_id',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Deleting field 'Place.foursq_primary_cat'
        db.delete_column(u'dataman_place', 'foursq_primary_cat_id')

        # Removing M2M table for field foursq_categories on 'Place'
        db.delete_table(db.shorten_name(u'dataman_place_foursq_categories'))


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
            'credentials': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['datascrape.ServiceInfo']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        u'datascrape.service': {
            'Meta': {'object_name': 'Service'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'datascrape.serviceinfo': {
            'Meta': {'object_name': 'ServiceInfo'},
            'access_key': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datascrape.Service']"}),
            'shared_secret': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'uid': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['dataman']