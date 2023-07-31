from datetime import datetime, date

from django.utils.timesince import timesince
from rest_framework import serializers
from haberler.models import Makale


class MakaleSerializer(serializers.ModelSerializer):
    time_since_pub = serializers.SerializerMethodField()

    class Meta:
        model = Makale
        fields = '__all__'
        # fields = ['yazar', 'baslik', 'metin'] #show this fields
        # exclude = ['yazar', 'baslik', 'metin'] #hide this fields
        read_only_fields = ['id', 'yaratilma_tarihi', 'guncellenme_tarihi']

    def get_time_since_pub(self, obj):
        if obj.aktif:
            return timesince(obj.yayimlanma_tarihi, datetime.now())
        return 'aktif degil'

    def validate_yayimlanma_tarihi(self, obj):
        if obj > date.today():
            raise serializers.ValidationError("Yayimlanma ileri bir tarih olamaz!")
        return obj

    def validate_baslik(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(f'Başlık 20 karakterden az olamaz. karakter sayısı: {len(value)}')
        return value


class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayimlanma_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only=True)
    guncellenme_tarihi = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        print(validated_data)
        return Makale.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.yazar = validated_data.get('yazar', instance.yazar)
        instance.baslik = validated_data.get('baslik', instance.baslik)
        instance.aciklama = validated_data.get('aciklama', instance.aciklama)
        instance.metin = validated_data.get('metin', instance.metin)
        instance.sehir = validated_data.get('sehir', instance.sehir)
        instance.yayimlanma_tarihi = validated_data.get('yayimlanma_tarihi', instance.yayimlanma_tarihi)
        instance.aktif = validated_data.get('aktif', instance.aktif)
        instance.save()
        return instance

    def validate(self, data):
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError('Başlık ve Açıklama aynı olamaz.')
        return data

    def validate_baslik(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(f'Başlık 20 karakterden az olamaz. karakter sayısı: {len(value)}')
        return value
