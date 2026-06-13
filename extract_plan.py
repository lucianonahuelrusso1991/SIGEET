import os
import json
from google import genai
from google.genai import types

def extract_plan():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Falta GEMINI_API_KEY")
        return

    client = genai.Client(api_key=api_key)

    # Upload the file
    print("Uploading PDF...")
    try:
        uploaded_file = client.files.upload(file="plan.pdf", config={'display_name': 'plan_estudio'})
        print(f"Uploaded as {uploaded_file.name}")
    except Exception as e:
        print(f"Upload failed: {e}")
        return

    prompt = """
    Extrae el plan de estudios completo de este PDF.
    Devuélvelo estrictamente en formato JSON válido, sin bloques de código Markdown ni texto adicional.
    La estructura debe ser:
    {
      "nombre_plan": "Profesorado de...",
      "materias": [
        {
          "año_dictado": 1,
          "nombre": "Nombre de la materia",
          "correlativas_cursada": ["Nombre exacto de materia 1", "Nombre exacto de materia 2"],
          "correlativas_aprobada": ["Nombre exacto de materia 3"]
        }
      ]
    }
    Asegúrate de deducir correctamente los años (1, 2, 3, 4...) de cada materia basándote en la estructura visual del plan, y normaliza los nombres exactos en los arreglos de correlativas.
    """

    print("Generating content...")
    response = client.models.generate_content(
        model='gemini-2.5-pro',
        contents=[uploaded_file, prompt],
        config=types.GenerateContentConfig(
            temperature=0.0
        )
    )

    try:
        data = response.text
        # Clean markdown if present
        if data.startswith("```json"):
            data = data[7:-3]
        elif data.startswith("```"):
            data = data[3:-3]
            
        with open('plan_extracted.json', 'w', encoding='utf-8') as f:
            f.write(data.strip())
        print("Success! Saved to plan_extracted.json")
    except Exception as e:
        print(f"Failed to save JSON: {e}")

if __name__ == "__main__":
    extract_plan()
