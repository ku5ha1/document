import os
from pypdf import PdfReader

def extract_and_save_text(pdf_path: str):
    
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        reader = PdfReader(pdf_path)
        
        full_text = ""
      
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
            
        base_name = os.path.basename(pdf_path)
        file_name = os.path.splitext(base_name)[0] + ".txt"

        output_path = os.path.join(output_dir, file_name)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
            
        return full_text
        
    except Exception as e:
        print(f"An error occurred: {e}")