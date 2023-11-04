from rest_framework import serializers
from social.models import FacebookPost, LinkedInPost, TwitterPost

class FacebookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookPost
        fields = '__all__'

class LinkedInPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedInPost
        fields = '__all__'

class TwitterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterPost
        fields = '__all__'
