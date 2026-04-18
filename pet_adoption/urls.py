from django.contrib import admin
import debug_toolbar
from django.urls import path, include
# from .views import api_root_view 
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi  
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.generic import RedirectView
# from debug_toolbar.toolbar import debug_toolbar_urls                                                                                                                          
                                                                                                                           

# Swagger/OpenAPI configurationJWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU1NjI2MjI5LCJpYXQiOjE3NTU1Mzk4MjksImp0aSI6ImI4ODc3Nzc2MTFkNjQ2OTBhM2Y4Zjc4NzhhOTI2MzA2IiwidXNlcl9pZCI6IjIifQ.QXMpKvtuOFKaaNOLtWLJvXr5gebByb2X-EJ4D4IGuFo" }
schema_view = get_schema_view(
    openapi.Info(
        title="Pet Adoption API",
        default_version='v1',
        description="API Documentation for Pet Adoption Project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@petadoption.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', api_root_view),
    path('', include('core.urls')),
    path('shop/', include('orders.web_urls')),
    path('users/', include('users.urls')),
    path('api/v1/', include('api.urls'), name='api-root'), 
    # path("api/v1/accounts/", include("users.urls")),
    path("api/v1/", include("djoser.urls")),
    path('users/', include('users.urls')),
    path("pets/", include("pets.urls")),
    path('cart/', RedirectView.as_view(pattern_name='orders:cart_detail', permanent=False), name='cart_redirect'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/login/', TokenObtainPairView.as_view(), name='users_login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('__debug__/', include(debug_toolbar.urls)),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# # ]+ debug_toolbar_urls()
# # Include debug toolbar URLs only in DEBUG mode
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)