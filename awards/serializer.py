from rest_framework import serializers
from .models import Profile,Post

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('user', 'rate')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user', 'profile')
