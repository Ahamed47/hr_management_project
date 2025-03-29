from django.core.management.base import BaseCommand
from employees.utils import check_expiring_visas

class Command(BaseCommand):
    help = "Check expiring visas and send alerts"

    def handle(self, *args, **kwargs):
        check_expiring_visas()
        self.stdout.write(self.style.SUCCESS("Visa expiry check completed."))
