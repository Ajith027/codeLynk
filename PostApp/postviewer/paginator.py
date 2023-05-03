from rest_framework.response import Response
from rest_framework import pagination


class Pagination(pagination.PageNumberPagination):

    def __init__(self,x):
        self.page_size=x

    def get_paginated_response(self,data):
        return Response({
            'status': 'success',
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data,})