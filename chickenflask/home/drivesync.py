from __future__ import print_function
import pickle
import io
import os.path
import mammoth
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config import BASE_PATH

# If modifying these scopes, delete the file token.pickle.
CREDS_PATH = BASE_PATH / 'chickenflask/home'
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def get_binaries_from_id(file_id, last_sync=None):
    """Takes doc id, returns update type ('rst' or 'html') and byte like obj

    TODO update only if file changed since last sync
    :returns
        str: 'no_update', 'rst', 'html'
            update type
        bytes:
            rst or html bytes if change, else b''
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(CREDS_PATH / 'token.pickle'):
        with open(CREDS_PATH / 'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_PATH / 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(CREDS_PATH / 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Metadata request to get mimeType and modifiedTime
    meta_request = service.files().get(fileId=file_id, fields='mimeType, modifiedTime')
    mime_type = meta_request.execute()['mimeType']
    last_modified = meta_request.execute()['modifiedTime']

    # Return with no_change if file wasnt modified since last update
    if last_sync and last_sync > last_modified:
        return 'no_update', b''

    # Check mime type and make appropriate request for content
    assert mime_type in ['text/plain', 'application/vnd.google-apps.document', 'text/markdown'], \
        f'Mime type "{mime_type}" not supported. Check to make sure file is a txt/rst or a doc.'

    if mime_type in ['text/plain', 'text/markdown']:
        update_type = 'rst'
        request = service.files().get_media(fileId=file_id)

    else:
        update_type = 'docx'
        mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        request = service.files().export_media(fileId=file_id, mimeType=mime_type)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    return update_type, fh


def process_docx(b, file_url=None):
    """Make a rst-compatible string from docx binary. Uses first line as title."""

    html = mammoth.convert_to_html(b).value
    if html[:3] == '<p>':
        title = html.split('</p>')[0].split('>')[-1]
    else:
        first_tag = html[:4]
        title = html.split('</' + first_tag[-3:])[0].split('>')[-1]

    return f'{title}\n{"=" * len(title)}\n\n.. raw:: html\n\n   ' + html


def process_txt(b, file_url=None):
    text = b.getvalue().decode("utf-8")
    #add comment for url and stuff
    return text.replace('\r', '')


def get_id_from_url(url):
    if '?id=' in url:
        file_id = url.split('?id=')[-1]
    else:
        file_id = url.split('/')[-2]
    return file_id


def sync_new_file(url):
    id = get_id_from_url(url)
    status, binary = get_binaries_from_id(id)

    if status == 'rst':
        content_type = 'markdown'
        content = binary.getvalue().decode("utf-8")
    elif status == 'docx':
        content_type = 'html'
        content = mammoth.convert_to_html(binary).value
    else:
        raise Exception('Fetching from drive failed')

    return content, content_type



if __name__ == '__main__':
    file_id = '1zay-X3cZ0WEPMEKk29Yx-x0yFjaghXtI7LOFPmebFxg' # doc
    #file_id = '1lpHeU1-91uHLTFtTZSfPma2OSCeSGK8s' # rst/txt

    status, binary = get_binaries_from_id(file_id)
    print(status)
    # print(process_txt(binary))
    #fi = process_docx(binary)
    #save_to_rst(fi, 'fromdocx.rst')




