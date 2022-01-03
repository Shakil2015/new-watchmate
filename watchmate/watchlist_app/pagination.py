from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination
from rest_framework.response import Response
class WatchListPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size =2
    last_page_strings = ('end',)
class WatchListOffSetPagination(LimitOffsetPagination):
    default_limit =3
    max_limit = 5
    limit_query_param = 'records'
    offset_query_param = 'start'

class WatchListCursorPagination(CursorPagination):
    page_size =3
    ordering = '-created'
    cursor_query_param = 'records'
class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
        