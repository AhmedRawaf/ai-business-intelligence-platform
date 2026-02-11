from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.kpi.models import KPIDataSet, KPIRecord
from apps.organizations.models import Membership, Organization


class Command(BaseCommand):
    help = "Seed demo organization, users, and Saudi KPI data"

    def handle(self, *args, **options):
        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True},
        )
        admin_user.set_password("admin12345")
        admin_user.save()

        analyst_user, _ = User.objects.get_or_create(username="analyst", defaults={"email": "analyst@example.com"})
        analyst_user.set_password("analyst12345")
        analyst_user.save()

        org, _ = Organization.objects.get_or_create(name="Saudi Retail Group", slug="saudi-retail-group")
        Membership.objects.get_or_create(user=admin_user, organization=org, defaults={"role": Membership.Roles.ADMIN})
        Membership.objects.get_or_create(user=analyst_user, organization=org, defaults={"role": Membership.Roles.ANALYST})

        dataset, _ = KPIDataSet.objects.get_or_create(
            organization=org,
            name="saudi_sales_demo.csv",
            defaults={"uploaded_by": admin_user, "source_file": "kpi/seed.csv", "columns": [], "row_count": 0},
        )
        if dataset.records.count() == 0:
            rows = [
                {"branch": "Riyadh", "month": "2026-01", "category": "Electronics", "sales": 120000},
                {"branch": "Dammam", "month": "2026-01", "category": "Electronics", "sales": 90000},
                {"branch": "Jeddah", "month": "2026-01", "category": "Home", "sales": 76000},
                {"branch": "Riyadh", "month": "2026-02", "category": "Home", "sales": 134000},
                {"branch": "Jeddah", "month": "2026-02", "category": "Electronics", "sales": 88000},
                {"branch": "Dammam", "month": "2026-02", "category": "Fashion", "sales": 62000},
            ]
            KPIRecord.objects.bulk_create(
                [KPIRecord(dataset=dataset, organization=org, data=row) for row in rows]
            )
            dataset.columns = ["branch", "month", "category", "sales"]
            dataset.row_count = len(rows)
            dataset.save(update_fields=["columns", "row_count"])

        self.stdout.write(self.style.SUCCESS("Demo seed complete."))
