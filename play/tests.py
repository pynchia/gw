from django.test import TestCase
from play.models import Subject, Feature, Player, Game, BoardElement


class TestFeatures(TestCase):

    def setUp(self):
        self.subj = Subject.objects.get(pk=1)  # Alex

    def test_alex_features(self):
        n = self.subj.feature_set.count()
        self.assertEqual(n, 6)

