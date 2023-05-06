from PIL import Image, ImageDraw, ImageFont
from rest_framework.authentication import SessionAuthentication
from .paginator import Pagination


def paginationfun(pageitems,data,request):
    paginator = Pagination(pageitems)
    page_data = paginator.paginate_queryset(data, request)
    return paginator.get_paginated_response(page_data)

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
