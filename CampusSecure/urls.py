from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", include("django_prometheus.urls",)),
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'favicon.ico')),

    # apps
    path("accounts/",include(("accounts.urls", "accounts"), namespace="accounts"),),
    path("documents/", include(("documents.urls", "documents"), namespace="documents")),
    path("exams/", include(("exams.urls", "exams"), namespace="exams")),
    path("audit-logs/", include(("audit.urls", "audit"), namespace="audit")),
    path("school/", include(("school.urls", "school"), namespace="school")),
    path("students/", include(("students.urls", "students"), namespace="students")),
    path("payment/", include(("payment.urls", "payment"), namespace="payment")),
    path("sentry/", include(("integrations.urls", "integrations"), namespace="integrations")),
    
]





"""Rest_Framework AutoDocs URLS """
from accounts.views import PublicSchemaView, PublicSwaggerView, PublicRedocView

urlpatterns += [
    # Patterns
    path('api/schema/', PublicSchemaView.as_view(), name='schema'),
    
    # Swagger UI:
    path('api/swagger-ui/', PublicSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', PublicRedocView.as_view(url_name='schema'), name='redoc'),
]

# media url
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# debug urls
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path("dev/", include(("devtools.urls", "devtools"), namespace="devtools")),
    ]