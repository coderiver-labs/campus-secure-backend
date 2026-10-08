import logging
from utils.middleware.request_context import get_current_request


# Request Filtering


class RequestContextFilter(logging.Filter):
    def filter(self, record):
        request = get_current_request()

        record.request_id = "-"
        record.user_id = "-"
        record.ip = "-"

        if request:
            record.request_id = getattr(request, "request_id", "-")
            
            # client ip read
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                # akhne onek gula ip ar caine thakte pare , akhne prothoomtai real ip
                record.ip = x_forwarded_for.split(',')[0].strip()
            else:
                # jodi kono caine na thake tahole jeta ase setai rekhe deya hobe
                record.ip = request.META.get("REMOTE_ADDR", "-")

            if hasattr(request, "user") and request.user.is_authenticated:
                record.user_id = str(getattr(request.user, "uuid"))

        return True


