import docx2txt
import nltk
import re

from pdfminer.high_level import extract_text

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def extract_docx(docx_path):
    txt = docx2txt.process(docx_path)
    if txt:
        return txt.replace('\t', ' ')
    else:
        return None
    
def extract_names(txt):
    names = []

    for i in nltk.sent_tokenize(txt):
        for j in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(i))):
            if hasattr(j,'label') and j.label() == "PERSON":
                names.append(' '.join(k[0] for k in j.leaves()))
    
    return names

def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)

def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
 
    if phone:
        number = ''.join(phone[0])
 
        if resume_text.find(number) >= 0 and len(number) <= 16:
            return number
        else: 
            return None

if __name__ == '__main__':
    text = extract_text_from_pdf('./resume_2.pdf')
    names = extract_names(text)
    phone_number = extract_phone_number(text)
    email_address = extract_emails(text)

    if names:
        print('Name:',names[3])
    else:
        print('No name found')

    if phone_number:
        print('Phone Number:',phone_number)
    else:
        print("no phone number found")
    
    if email_address:
        print('Email_address:',email_address[0])
    else:
        print("no email address found")

