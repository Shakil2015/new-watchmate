from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins,generics
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django.shortcuts import render
from watchlist_app.models import WatchList,StreamPlatform,Review
from watchlist_app.serializers import WatchListSerializer,StreamPlatformSerializer,ReviewSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from watchlist_app.permissions import IsAdminOrReadOnly,IsReviewUserOrReadOnly
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle,ScopedRateThrottle
from watchlist_app.throttlings import ReviewCreateThrottle,ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from watchlist_app.pagination import WatchListPagination,WatchListOffSetPagination,WatchListCursorPagination,CustomPagination

class UserReviewApiView(generics.ListAPIView):
    #queryset = Review.objects.all()
    serializer_class =ReviewSerializer
    #permission_classes = [IsAuthenticated]
    #throttle_classes = [ReviewCreateThrottle,AnonRateThrottle]

    def get_queryset(self):
        #username=self.kwargs['username']
        username = self.request.query_params.get('username') 
        return Review.objects.filter(review_user__username=username)

class ReviewCreateApiView(generics.CreateAPIView):
    serializer_class= ReviewSerializer
    permission_classes = [IsAuthenticated]
    #throttle_classes = [ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk=self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_query = Review.objects.filter(watchlist=movie,review_user = review_user)
        if review_query.exists():
            raise ValidationError("This user reviews already")
        if movie.number_rating == 0:
            movie.rating_avg = serializer.validated_data['rating']
        else:
            movie.rating_avg = (movie.rating_avg+serializer.validated_data['rating'])/2
        movie.number_rating = movie.number_rating + 1
        movie.save()
        serializer.save(watchlist=movie,review_user = review_user)
class ReviewListApiView(generics.ListAPIView):
    #queryset = Review.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']
    serializer_class =ReviewSerializer
    #permission_classes = [IsAuthenticated]
    #throttle_classes = [ReviewCreateThrottle,AnonRateThrottle]

    def get_queryset(self):
        pk=self.kwargs.get('pk')
        return Review.objects.filter(watchlist=pk)
class ReviewDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsReviewUserOrReadOnly]
    queryset = Review.objects.all()
    serializer_class =ReviewSerializer
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'review-details'

class StreamPlatformApiView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

class StreamPlatformDetailsApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

class Watchlist(generics.ListCreateAPIView):
    #permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    #pagination_class = CustomPagination
    #Filtering
    #filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['title','platform__name']

    #searching
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['^title','=platform__name']

    # #ordering 
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['rating_avg','number_rating']
    #throttle_classes = [AnonRateThrottle,UserRateThrottle]

class WatchListApiView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
    
class WatchListDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer


#generic APIView

# class ReviewApiView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
# class ReviewDetailApiView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# Classbase APIView

# class StreamPlatformApiView(APIView):
#     def get(self, request):
#         streamplatformlist = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(streamplatformlist,many=True)
#         return Response(serializer.data)
#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
# class StreamPlatformDetailsApiView(APIView):
#     def get(self, request,pk):
#         streamplatform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(streamplatform)
#         return Response(serializer.data)
#     def put(self, request,pk):
#         streamplatform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(streamplatform,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# class WatchListApiView(APIView):

#     def get(self,request):
#         WatchLists = WatchList.objects.all()
#         serializer = WatchListSerializer(WatchLists,many=True)
#         return Response(serializer.data)
#     def post(self,request):
#         data = request.data
#         serializer = WatchListSerializer(data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=200)
#         else:
#             return Response(serializer.errors,status=404)
# class WatchListDetailApiView(APIView):
#     def get(self,request,pk):
#         watchlist = WatchList.objects.get(pk=pk)
#         serializer = WatchListSerializer(watchlist)
#         return Response(serializer.data)
#     def put(self,request,pk):
#         request_data = request.data
#         prev_data = WatchList.objects.get(pk=pk)
#         serializer = WatchListSerializer(prev_data,data=request_data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#     def delete(self,request,pk):
#         watchlist = WatchList.objects.get(pk=pk)
#         watchlist.delete()
#         return Response(status=404)


#Functional view.....................

# @api_view(['GET','POST'])
# def WatchList_list(request):

#     if request.method == 'GET':
#         WatchLists = WatchList.objects.all()
#         serializer = WatchListSerializer(WatchLists,many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         data = request.data
#         serializer = WatchListSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=201)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET','PUT','DELETE'])
# def WatchList_details(request,pk):

#     if request.method == 'GET':
#         WatchList = WatchList.objects.get(pk=pk)
#         serializer = WatchListSerializer(WatchList)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         request_data = request.data
#         data = WatchList.objects.get(pk=pk)
#         serializer = WatchListSerializer(data,data=request_data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=201)
#         else:
#             return Response(serializer.errors,status=400)
            
#     elif request.method=='DELETE':
#         data = WatchList.objects.get(pk=pk)
#         data.delete()
#         return Response(status=204)


