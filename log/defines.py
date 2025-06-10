from log.models import Log
from utils.funcs import get_client_ip, get_client_device


def save_log(request, type=None, view=None, log=None):
    try:
        Log.objects.create(
            type=type,
            view=view,
            request=request.build_absolute_uri(),
            body=request.POST,
            log=log,
            ip=get_client_ip(request),
            device=get_client_device(request)
        )

    except Exception as e:
        print(e)
