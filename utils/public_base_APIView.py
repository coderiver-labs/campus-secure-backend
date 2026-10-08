from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny


# other class and logic
from auth.csrf_authentication import CSRFAuthentication
from rest_framework.throttling import ScopedRateThrottle
# create public api view


# Base  Views
class BaseGenericMixinView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    pass



# views
class PublicGenericAPIView(GenericAPIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "api"

    permission_classes = [AllowAny]
    authentication_classes = [CSRFAuthentication]


class PublicGenericMixinView(BaseGenericMixinView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "api"
    
    permission_classes = [AllowAny]
    authentication_classes = [CSRFAuthentication]



