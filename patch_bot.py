import codecs
import re

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_bot = r"""def api_chatbot\(request\):
    if request\.method == 'POST':
        try:
            data = json\.loads\(request\.body\)
            mensaje = data\.get\('mensaje', ''\)
            alumno_id = data\.get\('alumno_id', 1\) 
            respuesta_ia = procesar_mensaje_chatbot\(mensaje, alumno_id\)
            return JsonResponse\(\{'respuesta': respuesta_ia\}\)
        except Exception as e:
            return JsonResponse\(\{'respuesta': f"Error interno: \{str\(e\)\}"\}, status=500\)
    return JsonResponse\(\{'error': 'Solo POST permitido'\}, status=405\)"""

new_bot = """@login_required
@csrf_exempt
def api_chatbot(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mensaje = data.get('mensaje', '')
            
            # Seguridad: Forzar el ID del alumno logueado si es un alumno
            if hasattr(request.user, 'perfil_alumno'):
                alumno_id = request.user.perfil_alumno.id
            else:
                alumno_id = data.get('alumno_id', 1) # Fallback para admin/docente probando
                
            respuesta_ia = procesar_mensaje_chatbot(mensaje, alumno_id)
            return JsonResponse({'respuesta': respuesta_ia})
        except Exception as e:
            return JsonResponse({'respuesta': f"Error interno: {str(e)}"}, status=500)
    return JsonResponse({'error': 'Solo POST permitido'}, status=405)"""

content = re.sub(old_bot, new_bot, content)

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
