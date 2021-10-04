from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Blog, LikedBlogs
from .serializers import BlogSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@api_view(['POST'])
def register(request):

    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error':serializer.errors})
    serializer.save()
    user = User.objects.get(username=serializer.data['username'])
    token = Token.objects.get_or_create(user=user)
    return Response({"payload":serializer.data,"token": str(token)})



@api_view(['GET'])
# @permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def getAllBlogs(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def getBlogById(request,pk):
    blog = Blog.objects.get(id=pk)
    serializer = BlogSerializer(blog, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def getBlogByUser(request):
    blog = Blog.objects.filter(user=request.user)
    serializer = BlogSerializer(blog, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def createBlog(request):
    serializer = BlogSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'error':serializer.errors})
    serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def updateBlog(request, pk):
    # blogs = Blog.objects.filter(user=request.user.id)
    # print(blogs.first())
    blog = Blog.objects.get(id=pk)

    if blog.user != request.user:
        return Response({'error':'Inaccessible Blog'})
    serializer = BlogSerializer(instance=blog, data=request.data)
    if not serializer.is_valid():
        return Response({'error':serializer.errors})
    serializer.save()
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
@authentication_classes([TokenAuthentication])
def updateBlogAdmin(request, pk):
    # blogs = Blog.objects.filter(user=request.user.id)
    # print(blogs.first())
    blog = Blog.objects.get(id=pk)
    serializer = BlogSerializer(instance=blog, data=request.data)
    if not serializer.is_valid():
        return Response({'error':serializer.errors})
    serializer.save()
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def likeBlog(request, pk):

    user = request.user
    blog = Blog.objects.get(id=pk)

    like, created = LikedBlogs.objects.get_or_create(   # get_or_create will 
                                                        # itself do the job of 
                                                        # finding and creating if not exist
        user = user,
        blog = blog
    )
    if not created:
        return Response('Already Liked') #I don't wanted to show any error if existed earlier.
                                 #I just wanted to redirect.

    else:
        serializer = BlogSerializer(blog,many=False)
        serializer.like(pk)
        return Response('Liked Successfully')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def deleteBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    blog.delete()
    return Response('Deleted Successfully')


