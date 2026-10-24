"""Middleware для логирования запросов."""
import logging

logger = logging.getLogger('homework.requests')


class RequestLoggingMiddleware:
    """Логирует каждый HTTP-запрос."""

    def __init__(self, get_response):
        """Сохраняет get_response."""
        self.get_response = get_response

    def __call__(self, request):
        """Логирует запрос до и после обработки."""
        user = request.user.username if request.user.is_authenticated else 'anonymous'
        logger.info(
            '[%s] %s — user: %s',
            request.method, request.path, user,
        )
        response = self.get_response(request)
        logger.info(
            'Response %s for %s %s',
            response.status_code, request.method, request.path,
        )
        return response
