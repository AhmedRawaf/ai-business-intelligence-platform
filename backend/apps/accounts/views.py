from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.audit.services import log_action
from apps.common.rate_limit import check_rate_limit
from .serializers import CurrentUserSerializer


class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        check_rate_limit(f"login:{request.META.get('REMOTE_ADDR', 'unknown')}", limit=10, window_seconds=60)
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            log_action(
                actor=request.user if request.user.is_authenticated else None,
                organization=None,
                action="login",
                target_type="auth",
                target_id="token",
                metadata={"username": request.data.get("username", "")},
            )
        return response


class RefreshView(TokenRefreshView):
    pass


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)
