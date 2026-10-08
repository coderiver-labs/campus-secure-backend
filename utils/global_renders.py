from rest_framework.renderers import JSONRenderer


# Create Global Renders



# json response wrapper
class GlobalJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context: dict=None):
        response = renderer_context.get("response") if renderer_context else None

        # Skip error responses
        if response is not None and response.status_code < 400:
            # Only wrap if not already wrapped
            if not (isinstance(data, dict) and "success" in data):
                data = {
                    "success": True,
                    "data": data if data is not None else {},
                }

        return super().render(data, accepted_media_type, renderer_context)