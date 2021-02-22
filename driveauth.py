from chickenflask.notes.drivesync import get_binaries_from_id

if __name__ == '__main__':
    print('This tool should fix problems with Drive api authentication')
    print('Enter a file id (juste the id, not the url) and a browser window should open to complete the process')
    file_id = input('File id: ')
    status, binary = get_binaries_from_id(file_id)
    print(f'Done, fetched a {status} file.')

