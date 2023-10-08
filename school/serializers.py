from rest_framework import serializers

from school.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_set = LessonSerializer(many=True, read_only=True)
    total_lessons = serializers.SerializerMethodField()

    def get_total_lessons(self, obj):
        return obj.lesson_set.count()

    class Meta:
        model = Course
        fields = '__all__'



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
