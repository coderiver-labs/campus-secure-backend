from auth.csrf_authentication import CSRFAuthentication

# DRF
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny


# create base view hare



class BaseModelViewSet(ModelViewSet):
    # throttle_classes = [ScopedRateThrottle]
    throttle_scope = "api"

    lookup_field = "uuid"





class BasePublicModelViewSet(ModelViewSet):
    throttle_scope = "api"
    
    permission_classes = [AllowAny]
    authentication_classes = [CSRFAuthentication]

    lookup_field = "uuid"
    


class BaseCRUModelViewSet(ListModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    throttle_scope = "api"
    lookup_field = "uuid"


"""_________________School Related View___________________"""
class BaseSchoolViewSet(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    throttle_scope = "api"
    lookup_field = "uuid"
    


    
"""___________________ User Related VIew_____________________"""
class BaseUserRelatedInfoView(BaseCRUModelViewSet):
    ...
        


"""___________________FeePayment________________"""
class BasePaymentView(BaseCRUModelViewSet):
    ...




"""______________________Payment Related_____________"""
class BasePaymentRelatedView(ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet):
    throttle_scope = "api"
    lookup_field = "uuid"
    