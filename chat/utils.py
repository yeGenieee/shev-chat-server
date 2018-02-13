from channels.db import database_sync_to_async

from .exceptions import ClientError
from .models import Topic, TopicMessage, ChatRoom, ChatRoomMessage
from .serializers import TopicMessageSerializer, ChatRoomMessageSerializer


# This decorator turns this function from a synchronous function into an async one
# we can call from our async consumers, that handles Django DBs correctly.
# For more, see http://channels.readthedocs.io/en/latest/topics/databases.html
@database_sync_to_async
def get_room_or_error(room_id, user, room_type):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    # Check if the user is logged in
    # if not user.is_authenticated:
    #     raise ClientError("USER_HAS_TO_LOGIN")
    # Find the room they requested (by ID)
    room = None

    try:
        if room_type == "topics" or room_type == None:
            room = Topic.objects.get(pk=room_id)
        elif room_type == "chatrooms":
            room = ChatRoom.objects.get(pk=room_id)
            pass
    except Topic.DoesNotExist:
        raise ClientError("Topic ROOM_INVALID")
    except ChatRoom.DoesNotExist:
        raise ClientError("Chat ROOM_INVALID")

    # Check permissions
    # if room.staff_only and not user.is_staff:
    #     raise ClientError("ROOM_ACCESS_DENIED")

    return room


@database_sync_to_async
def get_previous_messages(room_id, user, room_type):
    response_json_data = None

    try:
        if room_type == "topics" or room_type == None:
            room = Topic.objects.get(pk=room_id)
            # We want to show the last 100 messages, ordered most-recent-last
            # (기존의 메시지 50개를 가져온다)
            queryset = TopicMessage.objects.filter(topic_id=room.id)
            qs = queryset.order_by("created_time")[:50]
            print("qs count: " + str(qs.count()))

            messages_serializer = TopicMessageSerializer(qs, many=True)

            response_json_data = {
                'messages_serializer': messages_serializer.data,
            }
            print(response_json_data)
        elif room_type == "chatrooms":
            room = ChatRoom.objects.get(pk=room_id)
            # We want to show the last 100 messages, ordered most-recent-last
            # (기존의 메시지 50개를 가져온다)
            queryset = ChatRoomMessage.objects.filter(chatRoom=room.id)
            qs = queryset.order_by("created_time")[:50]
            print("qs count: " + str(qs.count()))

            messages_serializer = ChatRoomMessageSerializer(qs, many=True)

            response_json_data = {
                'messages_serializer': messages_serializer.data,
            }
            print(response_json_data)
            pass

    except Topic.DoesNotExist:
        raise ClientError("Topic ROOM_INVALID")
    except ChatRoom.DoesNotExist:
        raise ClientError("Chat ROOM_INVALID")

    # Check permissions
    # if room.staff_only and not user.is_staff:
    #     raise ClientError("ROOM_ACCESS_DENIED")
    return response_json_data


# 스크롤을 올리면 가장 최신의 messages 50개를 반환한다
