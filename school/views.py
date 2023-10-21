import stripe
from django.conf import settings
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from school.models import Course, Lesson, Payment, Subscription
from school.paginators import SchoolPaginator
from school.permissions import IsOwner, IsManager, IsManagerNotCreate, IsSuperuser
from school.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer, \
    SuccessPaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = SchoolPaginator

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated, IsManagerNotCreate, IsSuperuser]
        elif self.action == 'update':
            permission_classes = [IsAuthenticated, IsManager | IsOwner | IsSuperuser]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsManager | IsOwner | IsSuperuser]
        elif self.permission_classes == 'list':
            permission_classes = [IsAuthenticated, IsManager | IsOwner | IsSuperuser]
        else:
            permission_classes = [IsAuthenticated, IsOwner | IsSuperuser]
        return [permission() for permission in permission_classes]


"""Контроллеры уроков"""


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsManager | IsOwner]
    pagination_class = SchoolPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsManager | IsOwner]


#  Создание урока
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsManagerNotCreate | IsSuperuser]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        if not new_lesson.owner:
            new_lesson.owner = self.request.user
        new_lesson.save()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsManager | IsOwner | IsSuperuser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsSuperuser]


"""Контроллеры оплаты курсов студентами"""


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]

    def create(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_KEY_PUBLISHED
        data = request.data
        print(data)
        if data.get('course_payment'):
            product = get_object_or_404(Course, pk=data['course_payment'])
        else:
            product = get_object_or_404(Lesson, pk=data['lesson_payment'])

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=[data['payment_method']],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': product.amount,
                        'product_data': {
                            'name': product.name,
                        },
                    },
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url='http://localhost:8000/' + reverse('school:success') + '?session_id={CHECKOUT_SESSION_ID}'
        )

        return Response({'payment_url': checkout_session.url}, status=status.HTTP_201_CREATED)


class PaymentSuccessView(generics.ListAPIView):
    serializer_class = SuccessPaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        session_id = self.request.GET.get('session_id')  # Получаем параметр session_id из URL
        if session_id:
            try:
                pay = Payment.objects.get(stripe_id=session_id)
                session = stripe.checkout.Session.retrieve(pay.stripe_id)
                pay.customer_email = session['customer_details']['email']
                pay.status = session['status']
                pay.save()
                return super().get(request, *args, **kwargs)
            except Payment.DoesNotExist:
                return Response({'error': 'Платеж не найден'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'session_id не передан в URL'}, status=status.HTTP_400_BAD_REQUEST)


# # def perform_create(self, serializer):
#     stripe.api_key = settings.STRIPE_KEY_PUBLISHED
#     # new_payment = serializer.
#     print(serializer['user'])
#     test_payment_intent = stripe.PaymentIntent.create(
#         amount=serializer["payment_amount"],
#         payment_method_types=serializer["payment_method"],
#         receipt_email=serializer["user"]['email'])
#     # test_payment_intent.save()
#     return Response(status=status.HTTP_200_OK, data=test_payment_intent)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course_payment', 'lesson_payment', 'payment_method')
    ordering_fields = ('payment_amount',)
    permission_classes = [IsAuthenticated]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentDestroyAPIView(generics.DestroyAPIView):
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]


"""Контролллеры подписок обновления студентов на курсы"""


class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionUpdateAPIView(generics.UpdateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionListAPIView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
