def notificaciones_context(request):
    if request.user.is_authenticated:
        from gestion.models import Notificacion
        unread_count = Notificacion.objects.filter(usuario=request.user, leida=False).count()
        return {'unread_notifications_count': unread_count}
    return {'unread_notifications_count': 0}
