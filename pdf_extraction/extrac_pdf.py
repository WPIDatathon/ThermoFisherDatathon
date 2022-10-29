import PyPDF2
import re
from pathlib import Path
import pprint 
import json


pp = pprint.PrettyPrinter(indent = 4)


def pdf_info(read_pdf):
    """
    Takes a formated PyPDF2 PDF and returns the pertinent information of said PDF
    ArgumentsL
    read_pdf: A .pdf previously formatted by PyPDF2
    returns:
    List of all of the attributes
    """
    pdf_info_dict = {}
    pdf_info = {}
    for key,value in read_pdf.documentInfo.items():
        pdf_info_dict[re.sub('/',"",key)] = value
    return pdf_info_dict

def pdf_text(read_pdf):
    text = ""
    for page in read_pdf.pages:
        text += page.extract_text()
    return text

if __name__ == "__main__":
    """
    Get the pdf details and print the Materials and Methods section
    """
    pdf_path = Path("../content/PDFs/gene_editing/doudna2022omicron.pdf")
    opener = open(pdf_path,"rb")
    pdf_file_reader = PyPDF2.PdfFileReader(opener)
    pp.pprint(pdf_info(pdf_file_reader))
    text = pdf_text(pdf_file_reader)

    search_param = "Materials and Methods"

    index_mat = text.find(search_param)
    print(text[index_mat:])