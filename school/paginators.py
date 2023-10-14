from rest_framework.pagination import PageNumberPagination


class SchoolPaginator(PageNumberPagination):
    page_size = 10
