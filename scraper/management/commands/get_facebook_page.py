# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from scraper.facebook.get_fb_posts_fb_group import scrapeFacebookPageFeedStatus
from django.conf import settings

app_id = settings.SOCIAL_AUTH_FACEBOOK_KEY
app_secret = settings.SOCIAL_AUTH_FACEBOOK_SECRET
group_id = "206291902739080"  # gumi

access_token = app_id + "|" + app_secret


class Command(BaseCommand):
    help = "My shiny new management command."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        scrapeFacebookPageFeedStatus(group_id, access_token)
