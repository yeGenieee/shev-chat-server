from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    GroupListAPIView,
    GroupDetailAPIView,

    TopicListViewSet,
    TopicDetailViewSet,

    ChatRoomListViewSet,
    ChatRoomDetailViewSet,
    # ChatRoomInviteAPIView,

    FileUploadView
)

topic_list = TopicListViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
topic_detail = TopicDetailViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    # 'patch': 'partial_update',
    'delete': 'destroy'
})

chatRoom_list = ChatRoomListViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
chatRoom_detail = ChatRoomDetailViewSet.as_view({
    'get': 'retrieve',
    # 'put': 'update',
    # 'patch': 'partial_update',
    'delete': 'destroy'
})


# API endpoints
urlpatterns = format_suffix_patterns([
    # api/group/:user_id
    # 사용자의 그룹 리스트를 보여준다
    url(r'^(?P<user_id>\d+)/$', GroupListAPIView.as_view(), name='group_list'),

    # api/group/:group_id/:user_id
    # 사용자 그룹의 Topic과 Chat list를 반환한다
    url(r'^(?P<group_id>\d+)/(?P<user_id>\d+)/$', GroupDetailAPIView.as_view(), name='group_detail'),

    ###########################################################################################

    # api/group/:group_id/topics [GET][POST]
    url(r'^(?P<group_id>\d+)/topics/$', topic_list, name='topic_list'),

    # api/group/:group_id/topics/:topic_id [GET][PUT][DELETE]
    url(r'^(?P<group_id>\d+)/topics/(?P<topic_id>\d+)/$', topic_detail, name='topic_detail'),

    ###########################################################################################

    # api/group/:group_id/chatrooms [GET][POST]
    url(r'^(?P<group_id>\d+)/chatrooms/$', chatRoom_list, name='chatRoom_list'),

    # api/group/:group_id/chatrooms/:chatroom_id [GET][DELETE]
    url(r'^(?P<group_id>\d+)/chatrooms/(?P<chatroom_id>\d+)/$', chatRoom_detail, name='chatRoom_detail'),

    # api/group/:group_id/chatrooms/:chatroom_id/invitation [POST]
    # url(r'^(?P<group_id>\d+)/chatrooms/(?P<chatroom_id>\d+)/invitation/$', ChatRoomInviteAPIView.as_view(), name='chatRoom_invitation'),
    ###########################################################################################

    # api/group/fileupload
    url(r'^fileupload/$', FileUploadView.as_view())
    # url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
])
