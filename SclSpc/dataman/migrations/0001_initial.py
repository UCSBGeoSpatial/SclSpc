# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'dataman_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal(u'dataman', ['User'])

        # Adding M2M table for field credentials on 'User'
        m2m_table_name = db.shorten_name(u'dataman_user_credentials')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm[u'dataman.user'], null=False)),
            ('serviceinfo', models.ForeignKey(orm[u'datascrape.serviceinfo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['user_id', 'serviceinfo_id'])

        # Adding model 'Location'
        db.create_table(u'dataman_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal(u'dataman', ['Location'])

        # Adding model 'Place'
        db.create_table(u'dataman_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataman.Location'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('venueid', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('foursq_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('foursq_cat_id', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('foursq_cat_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal(u'dataman', ['Place'])

        # Adding model 'Tag'
        db.create_table(u'dataman_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'dataman', ['Tag'])

        # Adding model 'CheckIn'
        db.create_table(u'dataman_checkin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataman.Location'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataman.Place'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataman.User'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datascrape.Service'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uid', self.gf('django.db.models.fields.BigIntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'dataman', ['CheckIn'])

        # Adding M2M table for field tags on 'CheckIn'
        m2m_table_name = db.shorten_name(u'dataman_checkin_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('checkin', models.ForeignKey(orm[u'dataman.checkin'], null=False)),
            ('tag', models.ForeignKey(orm[u'dataman.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['checkin_id', 'tag_id'])

        # Adding model 'Pic'
        db.create_table(u'dataman_pic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datascrape.Service'], null=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dataman.Location'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2400, null=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'dataman', ['Pic'])

        # Adding M2M table for field tags on 'Pic'
        m2m_table_name = db.shorten_name(u'dataman_pic_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pic', models.ForeignKey(orm[u'dataman.pic'], null=False)),
            ('tag', models.ForeignKey(orm[u'dataman.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pic_id', 'tag_id'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'dataman_user')

        # Removing M2M table for field credentials on 'User'
        db.delete_table(db.shorten_name(u'dataman_user_credentials'))

        # Deleting model 'Location'
        db.delete_table(u'dataman_location')

        # Deleting model 'Place'
        db.delete_table(u'dataman_place')

        # Deleting model 'Tag'
        db.delete_table(u'dataman_tag')

        # Deleting model 'CheckIn'
        db.delete_table(u'dataman_checkin')

        # Removing M2M table for field tags on 'CheckIn'
        db.delete_table(db.shorten_name(u'dataman_checkin_tags'))

        # Deleting model 'Pic'
        db.delete_table(u'dataman_pic')

        # Removing M2M table for field tags on 'Pic'
        db.delete_table(db.shorten_name(u'dataman_pic_tags'))


    models = {
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
            'foursq_cat_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'foursq_cat_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'foursq_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
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