import codecs

with codecs.open('gestion/views.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

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
    return JsonResponse({'error': 'Solo POST permitido'}, status=405)
"""

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if "def api_chatbot(request):" in line:
        start_idx = i
        break

if start_idx != -1:
    for i in range(start_idx, len(lines)):
        if "return JsonResponse" in lines[i] and "status=405" in lines[i]:
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    lines[start_idx:end_idx+1] = [new_bot]

with codecs.open('gestion/views.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
