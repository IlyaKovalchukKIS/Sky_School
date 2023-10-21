from django.urls import path, include
from rest_framework.routers import DefaultRouter
from school.apps import SchoolConfig
from school.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentCreateAPIView, PaymentUpdateAPIView, PaymentDestroyAPIView, \
    PaymentRetrieveAPIView, PaymentListAPIView, SubscriptionCreateAPIView, SubscriptionListAPIView, \
    SubscriptionRetrieveAPIView, SubscriptionUpdateAPIView, SubscriptionDestroyAPIView, PaymentSuccessView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = SchoolConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/list/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/detail/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/destroy/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_destroy'),
]

urlpatterns += [
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('payment/list/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/detail/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_detail'),
    path('payment/update/<int:pk>/', PaymentUpdateAPIView.as_view(), name='payment_update'),
    path('payment/destroy/<int:pk>/', PaymentDestroyAPIView.as_view(), name='payment_destroy'),
    path('payment/success/', PaymentSuccessView.as_view(), name='success'),
]

urlpatterns += [
    path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('subscription/list/', SubscriptionListAPIView.as_view(), name='subscription_list'),
    path('subscription/detail/<int:pk>/', SubscriptionRetrieveAPIView.as_view(), name='subscription_detail'),
    path('subscription/update/<int:pk>/', SubscriptionUpdateAPIView.as_view(), name='subscription_update'),
    path('subscription/destroy/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_destroy'),

]


urlpatterns += router.urls

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Your API description",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    # Другие URL-шаблоны вашего проекта...
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
