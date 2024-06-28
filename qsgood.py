import re
import fitz  # PyMuPDF

def extract_questions_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    questions = []
    
    for page_num in range(1, doc.page_count - 1):  # Ignoring the first and last page
        page = doc[page_num]
        text = page.get_text("text")
        
        # Split text into lines and process each line
        lines = text.split('\n')
        current_question = ""
        
        for line in lines:
            # Check if the line is a page instruction or copyright line
            if re.match(r'© UCLES', line) or re.match(r'\[Turn over\]', line):
                continue
            
            # Check if the line is part of the options
            if re.match(r'^[A-D]\s', line):
                continue
            
            # Check if the line starts a new question
            if re.match(r'^\d+\s', line):
                if current_question:
                    questions.append(current_question.strip())
                current_question = line
            else:
                current_question += " " + line
        
        # Add the last question if exists
        if current_question:
            questions.append(current_question.strip())
    
    # Filter out unwanted text like page numbers and instructions
    filtered_questions = []
    for question in questions:
        question = re.sub(r'© UCLES.*', '', question)
        question = re.sub(r'\[Turn over\]', '', question)
        question = question.strip()
        if question and not re.match(r'^\d{1,2}\s+\d{4}/\d{2}/[A-Z]/\d{2}$', question):
            filtered_questions.append(question)
    
    return filtered_questions

# Path to the PDF file
pdf_path = "0620_m22_qp_22.pdf"
questions = extract_questions_from_pdf(pdf_path)

# Output the questions separated by commas
output = ', '.join([f'"{question}"' for question in questions])
print(output)
