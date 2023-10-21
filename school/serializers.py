import os

import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework import serializers, status, response
from rest_framework.response import Response

from school.models import Course, Lesson, Payment, Subscription
from school.validators import UrlValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [UrlValidator(field='url_video')]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_set = LessonSerializer(many=True, read_only=True)
    subscription_set = SubscriptionSerializer(many=True, read_only=True)
    total_lessons = serializers.SerializerMethodField()
    validators = [UrlValidator(field='url_video')]

    def get_total_lessons(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SuccessPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False}
        }

# class PaymentCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = '__all__'
#         read_only_fields = ['date_payment']
#
#     def create(self, validated_data):
#         stripe.api_key = settings.STRIPE_KEY_PUBLISHED
#         product_id = validated_data.get('lesson_payment') if validated_data.get('lesson_payment') \
#             else validated_data.get('course_payment')
#         print(product_id)
#         # product = Course.objects.get(name=product_id) if Course.objects.get(name=product_id) \
#         #     else Lesson.objects.get(name=product_id)
#         checkout_session = stripe.PaymentIntent.create(
#             amount=2000,
#             currency="usd",
#             automatic_payment_methods={"enabled": True},
#         )
#         print(checkout_session)
#         return response(checkout_session)
