from .models import Video
from .serializers import VideoSerializer
from rest_framework.pagination import CursorPagination
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response


class VideoListView(APIView,CursorPagination):
    
    def get(self, request: Request):
        if not request.query_params.get('page_size'):
            request.query_params._mutable = True
            request.query_params['page_size'] = 10
            request.query_params._mutable = False

        data = Video.objects.all()

        self.ordering = "-published_datetime"
        self.page_size_query_param = "page_size"
        
        paginated_data = self.paginate_queryset(
            data, request, view=self)

        return Response({
                        'links': {
                            'next': self.get_next_link(),
                            'previous': self.get_previous_link()
                        },
                        'results': VideoSerializer(paginated_data, many=True).data
                        })
