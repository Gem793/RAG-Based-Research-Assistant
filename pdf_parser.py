from pypdf import PdfReader
def extract_text(pdf_path):
    reader=PdfReader(pdf_path)
    pages=[]
    for page_num,page in enumerate(reader.pages,start=1):
        text=page.extract_text()
        if text:
            pages.append({
                "page":page_num,
                "text":text
            }
            )
    return pages 