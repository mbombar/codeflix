import os
import pickle

from django.conf import settings
from django.core.management.base import BaseCommand
from graph import generate_graph


class Command(BaseCommand):
    help = "Generates the codeflix graph and serializes it to pickle bytestring"

    def add_arguments(self, parser):
        parser.add_argument(
            '--check',
            action='store_true',
            help='Check that contests marked as useless are indeed useless',
        )

        parser.add_argument(
            '--debug',
            action='store_true',
            help='Display the contest being considered. Useful for debugging.',
        )

    def handle(self, *args, **options):
        check = bool(options.get('check'))
        verbose = bool(options.get('debug'))

        with open(os.path.join(settings.BASE_DIR, "codeflix-graph"), "wb") as pgraph:
            pickle.dump(generate_graph.create_graph(check=check, verbose=verbose),
                        pgraph,
                        protocol=pickle.HIGHEST_PROTOCOL,
                        fix_imports=False,
                        )
