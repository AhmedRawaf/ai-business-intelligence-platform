import pandas as pd
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit.services import log_action
from apps.organizations.models import Membership
from .models import KPIDataSet, KPIRecord
from .serializers import KPIDataSetSerializer


class KPIDataSetListCreateView(generics.ListCreateAPIView):
    serializer_class = KPIDataSetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        memberships = Membership.objects.filter(user=self.request.user)
        org_ids = memberships.values_list("organization_id", flat=True)
        queryset = KPIDataSet.objects.filter(organization_id__in=org_ids).order_by("-created_at")
        organization_id = self.request.query_params.get("organization")
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)
        return queryset

    def perform_create(self, serializer):
        dataset = serializer.save(
            uploaded_by=self.request.user,
            name=serializer.validated_data["source_file"].name,
        )
        path = dataset.source_file.path
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        elif path.endswith(".xlsx"):
            df = pd.read_excel(path)
        else:
            raise ValueError("Unsupported dataset format.")

        dataset.columns = list(df.columns)
        dataset.row_count = len(df)
        dataset.save(update_fields=["columns", "row_count"])

        records = [
            KPIRecord(dataset=dataset, organization=dataset.organization, data=row)
            for row in df.fillna("").head(1000).to_dict(orient="records")
        ]
        KPIRecord.objects.bulk_create(records)

        log_action(
            actor=self.request.user,
            organization=dataset.organization,
            action="dataset_uploaded",
            target_type="dataset",
            target_id=str(dataset.id),
            metadata={"rows": dataset.row_count},
        )


class KPIAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        organization_id = request.query_params.get("organization")
        if not organization_id:
            return Response({"detail": "organization is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not Membership.objects.filter(user=request.user, organization_id=organization_id).exists():
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)

        records = KPIRecord.objects.filter(organization_id=organization_id).values_list("data", flat=True)
        payload = list(records)
        total_sales = 0.0
        branch_buckets = {}
        monthly_buckets = {}
        category_buckets = {}

        for row in payload:
            sales = float(row.get("sales", 0) or 0)
            branch = row.get("branch", "Unknown")
            month = row.get("month", "Unknown")
            category = row.get("category", "Unknown")
            total_sales += sales
            branch_buckets[branch] = branch_buckets.get(branch, 0.0) + sales
            monthly_buckets[month] = monthly_buckets.get(month, 0.0) + sales
            category_buckets[category] = category_buckets.get(category, 0.0) + sales

        return Response(
            {
                "summary": {
                    "total_sales": total_sales,
                    "records_count": len(payload),
                    "branches_count": len(branch_buckets),
                },
                "sales_by_branch": [{"name": key, "value": value} for key, value in branch_buckets.items()],
                "sales_by_month": [{"name": key, "value": value} for key, value in monthly_buckets.items()],
                "sales_by_category": [{"name": key, "value": value} for key, value in category_buckets.items()],
            }
        )
