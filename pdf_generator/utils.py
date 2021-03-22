import os

import PyPDF2


def remove_blank_page(file):

    file1 = f"media/results/test_{file}"

    file1_reader = open(file1, 'rb')
    file1_pdf_reader = PyPDF2.PdfFileReader(file1_reader)
    pdf_writer = PyPDF2.PdfFileWriter()
    num_pages = file1_pdf_reader.numPages
    page_to_delete = num_pages - 1

    if num_pages > 1:

        for page_num in range(file1_pdf_reader.numPages):
            if page_num != page_to_delete:
                pdf_writer.addPage(file1_pdf_reader.getPage(page_num))

        with open(f"media/results/{file}", "wb") as output:
            pdf_writer.write(output)

    else:
        for page_num in range(file1_pdf_reader.numPages):
            pdf_writer.addPage(file1_pdf_reader.getPage(page_num))

        with open(f"media/results/{file}", "wb") as output:
            pdf_writer.write(output)

    file1_reader.close()
    os.remove(file1)
