from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from snippet.models import Snippet, Tag
from snippet.serializers import (
                                    SnippetSerializer, 
                                    TagSerializer,
                                    SnippetDetailSerializer, 
                                    TagListSerializer
                                )


class SnippetViewSet(ViewSet):

    """
    Snippet ViewSet which handles all snippet actions
    Actions: create a snippet, list all snippets, retrive a snippet
             Updates a snippet, Deletes a snippet
    """

    def create(self, request):

        """
        Creates a new snippet

        Request:
        title - string
        content - string
        tag_title - string

        Response:
        title - string
        content - string
        create_at - datetime string
        updated_at - datetime string

        Path: /snippet/

        Method: POST

        Auth: JWT
        """

        serializer = SnippetSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def overview(self, request):

        """
        Lists all snippets

        Response:
        count - integer
        snippets - Snippet list

        Snippet:
        id - integer
        title - string
        url - string

        Path: /snippet/

        Method: GET

        Auth: JWT
        """
        
        snippets = Snippet.objects.all()
        serializer = SnippetDetailSerializer(snippets, many=True)
        response_data = {
            'count': snippets.count(),
            'snippets': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def retrive(self, request, pk):

        """
        Retrives a snippet

        Response:
        id - integer
        title - string
        create_at - datetime string
        updated_at - datetime string

        Path: /snippet/<id>/

        Method: GET

        Auth: JWT
        """

        try:
            snippet = Snippet.objects.get(id=pk)
        except Snippet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SnippetSerializer(instance=snippet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk):

        """
        Updates a snippet

        Request:
        title - string
        content - string
        tag_title - string

        Response:
        title - string
        content - string
        create_at - datetime string
        updated_at - datetime string

        Path: /snippet/<id>/

        Method: PATCH

        Auth: JWT
        """

        try:
            snippet = Snippet.objects.get(id=pk)
        except Snippet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.user != snippet.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = SnippetSerializer(instance=snippet, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk):

        """
        Deletes a snippet

        Path: /snippet/<id>/

        Method: DELETE

        Auth: JWT
        """
        
        try:
            snippet = Snippet.objects.get(id=pk)
            if request.user != snippet.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            snippet.delete()
        except Snippet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(ViewSet):

    """
    Tag ViewSet which handles some tag actions
    Actions: list all tags, retrive a tag
    """

    def overview(self, request):

        """
        Lists all tags

        Response:
        count - integer
        tags - Tag list

        Tag:
        id - integer
        title - string

        Path: /tag/

        Method: GET

        Auth: JWT
        """

        tags = Tag.objects.all()
        serializer = TagListSerializer(tags, many=True)
        response_data = {
            'count': tags.count(),
            'tags': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def retrive(self, request, pk):

        """
        Retrives a Tag with all its snippets

        Response:
        count - integer
        title - string
        snippets - Snippet list

        Snippet:
        id - integer
        title - string
        url - string

        Path: /tag/<id>/

        Method: GET

        Auth: JWT
        """

        try:
            tag = Tag.objects.get(id=pk)
        except Snippet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TagSerializer(instance=tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

