from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "per_page"
    max_page_size = 500

    def get_paginated_response(self, data):

        return Response({
            "total_items": self.page.paginator.count,
            "per_page": self.page.paginator.per_page,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,

            "first_page": self.request.build_absolute_uri(f"?page=1"),
            "last_page": self.request.build_absolute_uri(
                f"?page={self.page.paginator.num_pages}"
            ),

            "next": self.get_next_link(),
            "previous": self.get_previous_link(),

            "results": data,
        })
