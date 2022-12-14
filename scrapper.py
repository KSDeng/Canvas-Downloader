import requests, os, datetime
from contextlib import closing
from parameters import *

def get_sources():
    global ASPXAUTH
    global sandboxCookie
    global query_parameters
    if ASPXAUTH is None or sandboxCookie is None:
        print('set cookie and auth first')
        exit(1)
    ret = []
    res = requests.post('https://mediaweb.ap.panopto.com/Panopto/Services/Data.svc/GetSessions', headers={
        'cookie': f'.ASPXAUTH={ASPXAUTH}; sandboxCookie={sandboxCookie}'}, json=query_parameters)
    if res.status_code != 200:
        print('cookie & auth wrong or expired, reset them')
        exit(1)
    r = res.json()
    if r['d']['Results'] is None or len(r['d']['Results']) == 0:
        print('no results, check your cookie and auth')
        exit(1)
    for i in r['d']['Results']:
        ret.append((i['SessionName'], i['IosVideoUrl']))
    return ret

def download_video(download_url, download_path):
    video_name = os.path.basename(download_path)
    with closing(requests.get(download_url, timeout=10, verify=False, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        data_count = 0
        with open(download_path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                done_block = int((data_count / content_size) * 50)
                data_count = data_count + len(data)
                current_progress = (data_count / content_size) * 100
                print("\r %s [%s%s] %d%% " % (video_name+"---->", done_block * '█',
                                              ' ' * (50 - 1 - done_block), current_progress), end=" ")

if __name__ == '__main__':
    if not os.path.exists('output'):
        os.makedirs('output')
    sources = get_sources()
    with open(f'output/{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.txt', 'w') as f:
        for i in sources:
            f.write(f'{i[0]}: {i[1]}\n')
    f.close()
    for i in sources:
        save_path = '{}.mp4'.format(i[0]).replace('/','')
        if not os.path.exists(save_path):
            download_video('{}'.format(i[1]), save_path)


