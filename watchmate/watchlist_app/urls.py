from django.urls import path
from watchlist_app.views import (WatchListApiView,WatchListDetailApiView,
                                 StreamPlatformApiView,StreamPlatformDetailsApiView,
                                ReviewListApiView,ReviewDetailApiView,ReviewCreateApiView,UserReviewApiView,Watchlist)

app_name = 'testapp'

urlpatterns = [
    path('list/',WatchListApiView.as_view(),name='movie_list'),
    path('<int:pk>/',WatchListDetailApiView.as_view(),name='movie_details'),
    path('stream/',StreamPlatformApiView.as_view(),name='stream'),
    path('stream/<int:pk>/',StreamPlatformDetailsApiView.as_view(),name='stream_details'),

    path('new-watchlist/',Watchlist.as_view(),name='new-watchlist'),
    # path('review/<int:pk>/',ReviewDetailApiView.as_view(),name='review_detail'),
    path('stream/<int:pk>/review-create/',ReviewCreateApiView.as_view(),name='review_create'),
    path('stream/<int:pk>/review/',ReviewListApiView.as_view(),name='review'),
    path('stream/review/<int:pk>/',ReviewDetailApiView.as_view(),name='review_detail'),
    path('review/',UserReviewApiView.as_view(),name='user-review')
]