import os
import base64
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


def image_to_code(image):
    data = open(f'media/{image}', 'rb').read()  # read bytes from file
    data_base64 = base64.b64encode(data)  # encode to base64 (bytes)
    data_base64 = data_base64.decode()    # convert bytes to string

    html = '<img src="data:image/png;base64,' + data_base64 + '" id="p1img5">'   # embed in html
    return html
