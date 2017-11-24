from model_mommy import mommy

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase

User = get_user_model()


class TestPlayerListView(TestCase):
    base_url = reverse('player_list')

    def test_view_players_non_auth(self):
        response = self.client.get(self.base_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual('/accounts/login/?next=/players/list/', response.url)

    def test_view_players_non_couch(self):
        User.objects.create_player(username='player', password='player')
        self.client.login(username='player', password='player')
        response = self.client.get(self.base_url)
        self.assertEqual(403, response.status_code)

    def test_view_players_empty_list(self):
        User.objects.create_coach(username='coach', password='test')
        self.client.login(username='coach', password='test')
        response = self.client.get(self.base_url)
        self.assertEqual(200, response.status_code)
        self.assertTrue('No players found.' in str(response.content))

    def test_view_players(self):
        for x in range(3):
            mommy.make('players.Player')
        User.objects.create_coach(username='coach', password='test')
        self.client.login(username='coach', password='test')
        response = self.client.get(self.base_url)
        self.assertEqual(200, response.status_code)
        self.assertFalse('No players found.' in str(response.content))
        self.assertFalse('<ul class="pagination">' in str(response.content))

    def test_view_players_paginated(self):
        for x in range(settings.RESULTS_PER_PAGE + 1):
            mommy.make('players.Player')
        User.objects.create_coach(username='coach', password='test')
        self.client.login(username='coach', password='test')
        response = self.client.get(self.base_url)
        self.assertEqual(200, response.status_code)
        self.assertFalse('No players found.' in str(response.content))
        self.assertTrue('<ul class="pagination">' in str(response.content))
