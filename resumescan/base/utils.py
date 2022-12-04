from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
import re


keywordsSE = [
    "full stack", "back end", "javascript", "web design", "css", "php", "apis", "html", "ruby", "mysql", "python", "oracle", "mongodb", "databases", "node.js", "frameworks", "computer science", "programming", "coding", "c\+\+", "c#", "code optimizaion", "software design", 
    "jira", "distributed computing", "technical documentation", "technical", "project management", "agile", "agile", "software development", "git", "angularjs", "sql", "kotlin", "swift", "linux", "aws", "azure", "gcp", "xml", "css", "django", "php", 
    "laravel", "encryption", "unit testing", "system testing", "accountability", "flask", "problem-solving", "teamwork", "work ethic", "critical thinking", "creativity", "time management", "integration testing", "android", "clean", "scalable code", 
    "software systems", "debugging code", "debugging", "programming languages", "deploying software", "deploying", "github", "project management", "Postgresql"
    ]

def handle_uploaded_file(f):
    with open('static/uploads/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

#def job_decription_handler(f):



def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text

def getkeyWords(job_description, keywordsSE):
    extracted_keywords = set()

    for list_keyword in keywordsSE:
        keyword = list_keyword.replace("-", " ")
        for item in keyword.split():
            if re.search(item, job_description, re.IGNORECASE):
                extracted_keywords.add(list_keyword)
    return extracted_keywords