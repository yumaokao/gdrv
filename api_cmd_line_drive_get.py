#!/usr/bin/python
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import httplib2
import sys

from apiclient import errors
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

# For this example, the client id and client secret are command-line arguments.
    # 1037484691223.apps.googleusercontent.com oyJtlM6GhYvBQFvxstqLnDFI
client_id = "1037484691223.apps.googleusercontent.com"
client_secret = "oyJtlM6GhYvBQFvxstqLnDFI"

# The scope URL for read/write access to a user's calendar data
scope = 'https://www.googleapis.com/auth/drive'

flow = OAuth2WebServerFlow(client_id, client_secret, scope, "http://127.0.0.1")


def retrieve_me_files(service, query =""):
    """Retrieve a list of File resources.

    Args:
      service: Drive API service instance.
    Returns:
      List of File resources.
    """
    result = []
    page_token = None
    while True:
        try:
            param = {}
            if query != "":
                param['q'] = "title contains '%s'" % (query)
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(**param).execute()

            result.extend(files['items'])
            page_token = files.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError, error:
            print 'An error occurred: %s' % error
            break
    return result


def print_about(service):
    """Print information about the user along with the Drive API settings.

    Args:
      service: Drive API service instance.
    """
    try:
        about = service.about().get().execute()

        print 'Current user name: %s' % about['name']
        print 'Root folder ID: %s' % about['rootFolderId']
        print 'Total quota (bytes): %s' % about['quotaBytesTotal']
        print 'Used quota (bytes): %s' % about['quotaBytesUsed']
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def main():
    storage = Storage('credentials.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        #credentials = run(flow, storage)
        auth_uri = flow.step1_get_authorize_url()
        print "Please goto this link: [%s]" % auth_uri
        code = raw_input("Enter verrification code: ").strip()
        credentials = flow.step2_exchange(code)
        if credentials:
            storage.put(credentials)

    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = ""
    print "[%s]" % query

    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('drive', 'v2', http=http)
    print_about(service)

    me_files = retrieve_me_files(service, query)
    for fl in me_files:
        print "%s, %s, %s, %s" % (fl['title'], fl['id'], fl['fileSize'], fl['mimeType'])
        dlurl = fl['downloadUrl']
        if dlurl:
            resp, content = service._http.request(dlurl);
            print "Status: %s" % resp
            if resp.status == 200:
                f = open(fl['title'], 'w')
                f.write(content)
        

if __name__ == '__main__':
    main()
    # python authorized_api_cmd_line_drive.py
    # 1037484691223.apps.googleusercontent.com oyJtlM6GhYvBQFvxstqLnDFI
