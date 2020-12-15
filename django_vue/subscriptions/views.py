from rest_framework.response import Response
from rest_framework import generics
from . models import Posts
from . serializers import PostSerializer


class PostView(generics.RetrieveAPIView):
    queryset = Posts.objects.all()

    def get(self, request, *args, **kwargs):
        querySet = self.get_queryset()
        serializer = PostSerializer(querySet, many=True)
        return Response(serializer.data)
