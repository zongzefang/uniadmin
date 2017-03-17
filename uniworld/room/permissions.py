from rest_framework import permissions

def IsHost(request, room):
    return room.host==request.user

def IsParticipant(request,room):
    try:
        room.participants.get(id=request.user.id)
        return True
    except Exception:
        return False

