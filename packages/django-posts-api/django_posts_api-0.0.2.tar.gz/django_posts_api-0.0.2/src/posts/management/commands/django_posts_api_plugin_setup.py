from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Command for setup plugins'


def handle(self, *args, **options):
    self.stdout.write(self.style.SUCCESS('Successfully plugged'))
