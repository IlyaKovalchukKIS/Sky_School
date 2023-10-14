from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from school.models import Course, Lesson, Payment, Subscription
from school.paginators import SchoolPaginator
from school.permissions import IsOwner, IsManager, IsManagerNotCreate, IsSuperuser
from school.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, SubscriptionSerializer


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


class SubscriptionListAPIView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
