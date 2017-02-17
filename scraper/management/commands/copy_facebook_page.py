# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from scraper.facebook.get_fb_posts_fb_group import copyStatusToCore


class Command(BaseCommand):
    help = "My shiny new management command."

    # def add_arguments(self, parser):
    #     parser.add_argument('sample', nargs='+')

    def handle(self, *args, **options):
        copyStatusToCore()
