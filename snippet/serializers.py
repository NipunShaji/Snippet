
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from snippet.models import Tag, Snippet


class SnippetDetailSerializer(ModelSerializer):

    """
    Serializer class to fetch Snippet details
    Fields: id, title, url
    """

    url = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'url', )

    def get_url(self, obj):
        return reverse('api:snippet', kwargs={'pk': obj.id})


class TagSerializer(ModelSerializer):

    """
    Serializer to create and get details of tags
    Fields: title, id, snippets
    """

    snippets = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ('title', 'id', 'snippets')

    def get_snippets(self, obj):
        snippets = obj.snippets.all()
        return SnippetDetailSerializer(snippets, many=True).data


class TagListSerializer(ModelSerializer):

    """
    Serializer to list all Tags
    Fields: title, id
    """

    class Meta:
        model = Tag
        fields = ('title', 'id')


class SnippetSerializer(ModelSerializer):

    """
    Serializer to create, update and get detail of snippet
    Fields: id, title, content, created_at, updated_at, tag
    """


    tag_title = serializers.CharField(allow_blank=True, required=True, write_only=True)

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'user', 'tag', 'tag_title')
        extra_kwargs = {
            'user': {'write_only': True, 'required': False},
            'tag': {'write_only': True, 'required': False},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):

        """
        Creates a Tag with Tag as in tag_title and user as current User
        """

        validated_data['user'] = self.context['request'].user
        validated_data = self.create_or_get_tag(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):

        """
        Updates a Tag with Tag as in tag_title and user as current User
        """

        validated_data['user'] = self.context['request'].user
        validated_data = self.create_or_get_tag(validated_data)
        return super().update(instance, validated_data)

    def create_or_get_tag(self, validated_data):

        """
        Returns a new tag along with validated_data if available
        else create a new one and returns it
        """
        
        tag_title = validated_data.pop('tag_title')

        if Tag.objects.filter(title=tag_title).exists():
            return Tag.objects.get(title=tag_title)
        
        tag = TagSerializer(data={'title':tag_title})
        tag.is_valid(raise_exception=True)
        tag.save()
        validated_data['tag'] = tag
        return validated_data

    def validate_user(self, value):

        """
        Validated that the user updatig this snippet is the original owner
        """

        if self.instance and self.context['request'].user != self.instance.user:
            raise ValidationError(detail="You cannot edit other users snippet")
