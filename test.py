import base64


def image_to_code():
    data = open('Signatur_Roth.png', 'rb').read()  # read bytes from file
    data_base64 = base64.b64encode(data)  # encode to base64 (bytes)
    data_base64 = data_base64.decode()    # convert bytes to string

    html = '<img src="data:image/png;base64,' + data_base64 + '" id="p1img5">'   # embed in html
    print(html)
