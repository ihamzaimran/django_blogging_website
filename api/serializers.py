from rest_framework import serializers

from .models import Post, Vote

class PostSerializer(serializers.ModelSerializer):

    # posted_by = serializers.ReadOnlyField(source='posted_by.username')
    user_id = serializers.ReadOnlyField(source='posted_by.id')
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','title', 'url', 'created_on', 'posted_by', 'user_id', 'votes']
        read_only_fields = ['posted_by']

    def get_votes(self, post):
            return Vote.objects.filter(post=post).count()


class VoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vote
        fields = ['id']

