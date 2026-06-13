import fitz  # PyMuPDF
import sys

def main():
    try:
        doc = fitz.open("plan.pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        
        with open("plan_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Text extracted successfully to plan_text.txt")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
