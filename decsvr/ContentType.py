import mimetypes
# content code constants as integers
APPLICATION_JSON = 0
APPLICATION_XML = 1
APPLICATION_CSV = 2
PLANE_TEXT = 3
APPLICATION_HTML = 4
APPLICATION_JAVASCRIPT = 5
APPLICATION_CSS = 6
APPLICATION_PDF = 7
APPLICATION_ZIP = 8
APPLICATION_GZIP = 9
APPLICATION_IMAGE_ICO = 10

def get_mime_by_content_code(content_code):
    if type(content_code) is not int:
        return content_code
    
    if content_code == APPLICATION_JSON:
        return "application/json"
    elif content_code == APPLICATION_XML:
        return "application/xml"
    elif content_code == APPLICATION_CSV:
        return "application/csv"
    elif content_code == PLANE_TEXT:
        return "text/plain"
    elif content_code == APPLICATION_HTML:
        return "text/html"
    elif content_code == APPLICATION_JAVASCRIPT:
        return "application/javascript"
    elif content_code == APPLICATION_CSS:
        return "text/css"
    elif content_code == APPLICATION_PDF:
        return "application/pdf"
    elif content_code == APPLICATION_ZIP:
        return "application/zip"
    elif content_code == APPLICATION_GZIP:
        return "application/gzip"
    elif content_code == APPLICATION_IMAGE_ICO:
        return "image/x-icon"
    else:
        return "text/plain"

def get_content_type_by_file(file_path):
    return mimetypes.guess_type(file_path)[0] or 'text/plain'