from rest_framework import serializers

from .models import Hero


class HeroSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hero
        fields = ('id', 'name', 'alias')


# class CookieSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Cookies
#         fields = ('id', 'return_val')
