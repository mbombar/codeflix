from codeflix.views import graph
from codeforces.models import Problem
from django.db.models import IntegerField, Value
from recommendation import recommendation as rec
from rest_framework import generics

from .serializers import ProblemSerializer


class RecommendedProblemView(generics.ListAPIView):
    queryset = Problem.objects.none()
    serializer_class = ProblemSerializer

    def get_queryset(self):
        handle = self.kwargs.get('handle')
        if handle is None:
            return Problem.objects.none()
        problems = rec.recommendation(handle, graph[1], graph[0])[:5]
        q = Problem.objects.none()
        for i, pb in enumerate(problems):
            q = q.union(
                Problem.objects.filter(name=pb).annotate(
                    orderid=Value(i, output_field=IntegerField()))
            )
        return q.order_by('orderid')
