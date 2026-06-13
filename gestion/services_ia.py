import os
import json
from google import genai
from google.genai import types
from .models import TicketReclamo, Alumno

def procesar_mensaje_chatbot(mensaje_usuario, alumno_id):
    """
    Se comunica con Gemini, determina la intención del usuario y responde.
    Si el usuario quiere generar un ticket, usa Function Calling para crearlo.
    """
    # Intentamos obtener la API KEY del entorno (Debería configurarse en el sistema)
    api_key = os.environ.get("GEMINI_API_KEY", "TU_API_KEY_AQUI")
    
    # Iniciamos el cliente de Gemini
    client = genai.Client(api_key=api_key)

    # Obtenemos el alumno para el contexto
    try:
        alumno = Alumno.objects.get(id=alumno_id)
        contexto_alumno = f"Estás hablando con {alumno.nombre} {alumno.apellido} (DNI: {alumno.dni})."
    except Alumno.DoesNotExist:
        contexto_alumno = "Estás hablando con un estudiante anónimo."

    system_prompt = f"""
    Eres el Asistente Virtual Oficial de la Secretaría del Sistema de Gestión Escolar.
    {contexto_alumno}
    Tus tareas son:
    1. Responder preguntas frecuentes sobre fechas de finales (estamos en Nivel Terciario), correlatividades, inscripciones y trámites administrativos.
    2. Si el estudiante menciona un problema, queja o reclamo ("la nota está mal", "no me puedo inscribir", "quiero hacer un reclamo"), debes crear un ticket usando la función `crear_ticket_reclamo`.
    
    Sé amable, conciso y profesional.
    """

    # Función python que Gemini puede llamar
    def crear_ticket_reclamo(asunto: str, descripcion: str) -> str:
        """Crea un ticket de reclamo en la secretaría académica."""
        try:
            TicketReclamo.objects.create(
                alumno_id=alumno_id,
                asunto=asunto,
                descripcion=descripcion,
                estado='ABIERTO'
            )
            return "Ticket creado exitosamente. La secretaría lo revisará pronto."
        except Exception as e:
            return f"Error al crear el ticket: {str(e)}"

    # Configuramos el modelo y le pasamos nuestra función
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=mensaje_usuario,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=[crear_ticket_reclamo],
                temperature=0.3,
            )
        )
        
        # Si Gemini decidió llamar a la herramienta
        if response.function_calls:
            for function_call in response.function_calls:
                if function_call.name == "crear_ticket_reclamo":
                    # Extraer argumentos
                    kwargs = {arg: val for arg, val in function_call.args.items()}
                    resultado_tool = crear_ticket_reclamo(**kwargs)
                    
                    # Le devolvemos el resultado a Gemini para que genere la respuesta final humana
                    # O directamente le avisamos al usuario:
                    return f"He registrado tu reclamo en secretaría: {kwargs.get('asunto')}. {resultado_tool}"
                    
        return response.text
    except Exception as e:
        # Fallback en caso de que no haya API key o algo falle
        if "API_KEY_INVALID" in str(e) or "TU_API_KEY_AQUI" in api_key:
             return "Hola. El sistema de IA está en mantenimiento o la API KEY de Gemini no está configurada. Por favor contactá a la secretaría manualmente."
        return f"Ocurrió un error en el asistente: {str(e)}"
