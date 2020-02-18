from codeflix.views import baseurl
from codeforces.models import Problem
from rest_framework import serializers


class ProblemSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = '__all__'

    def get_url(self, obj):
        return baseurl.format(cid=obj.contest_id, index=obj.index)

    def get_tags(self, obj):
        return map(lambda t: t.name, obj.tags.all())
