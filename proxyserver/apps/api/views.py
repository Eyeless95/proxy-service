from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from proxyserver.apps.core.models import Proxy
from .permissions import IsOwnerOrReadOnly
from .serializers import ProxySerializer
from rest_framework import permissions, renderers, viewsets
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class ProxyViewSet(viewsets.ModelViewSet):
    queryset = Proxy.objects.all()
    serializer_class = ProxySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,
                          permissions.IsAdminUser,)

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'proxies': reverse('proxy-list', request=request, format=format)
    })