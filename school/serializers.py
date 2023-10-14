from rest_framework import serializers

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
