from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def api_posts_lists(request, *args, **kwargs):
    posts = [
        {"id": 1, "title": "Post 1"},
        {"id": 2, "title": "Post 2"}
    ]
    return Response(posts, status=status.HTTP_200_OK)
