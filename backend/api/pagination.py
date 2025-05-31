from rest_framework.pagination import PageNumberPagination

from foodgram_backend.settings import (
    MAX_PAGINATION_SIZE,
    COMMON_PAGINATION_SIZE,
)


class CustomPagination(PageNumberPagination):
    """Кастомная пагинация для API."""

    page_size_query_param = "limit"
    max_page_size = MAX_PAGINATION_SIZE
    page_size = COMMON_PAGINATION_SIZE
