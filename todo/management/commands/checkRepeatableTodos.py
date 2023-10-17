from django.core.management.base import BaseCommand

from todo.management import repeatableTodoUtils

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Check the repeatables to do and reset their state if necessary'


    def add_arguments(self, parser):
        parser.add_argument("--check-only", action="store_true",
                            help="Only check the repeatables, don't reset them")


    def handle(self, *args, **options):

        # get the value of the check-only option
        check_only = options["check_only"]

        logger.info(f"Check Repeatable Todos is run with --check-only={check_only}")

        repeatableTodoUtils.checkRepeatableTodos(check_only=check_only)
