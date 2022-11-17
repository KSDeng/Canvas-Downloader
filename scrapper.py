import requests
from cookies import get_video_cookies

request_url = "https://mediaweb.ap.panopto.com/Panopto/Services/Data.svc/GetSessions"
parameters = {
    "queryParameters":{
        "query": None,
        "sortColumn": 1,
        "sortAscending": False,
        "maxResults": 25,
        "page": 0,
        "startDate": None,
        "endDate": None,
        "folderID": "9161463d-6906-4a45-88b1-aee500604cf4",
        "bookmarked": False,
        "getFolderData": True,
        "isSharedWithMe": False,
        "isSubscriptionsPage": False,
        "includeArchived": True,
        "includeArchivedStateCount": True,
        "sessionListOnlyArchived": False,
        "includePlaylists": True
    }
}

# cookies
ASPXAUTH = 'C015E9543F7BCA82E7AEA82DA246A25AEB3E506C8BE\
793E06B5CA521118EDD9B256783A3C8D6C68F47975EC780DB381BB9D07\
C5983D602292CFB8D83132DD16CF22FAB5D9CD081BE77644F8850C467D09\
D527E6DBF62B208FC03A45A56AC8DF17001745A5B5C3FCA085A25B920229D\
9FD97DC064CC944945CF2B9F6ADF7C98B45C99AE3739F18A001DFEA2ECF3CF\
968E42D00775C0BF3EF4FF4FBF0AEEA1900E434F7B520E19DD3FFA4AB53C13E\
21CC067AB575E2C82E5A64259578815E3F496300A072BDD980E03893FDE06BD2C\
48ED6C20A396DB0E1C369DA933E2A0DD4CAEC608103E5F5096B139914F30391986D4'

csrfToken = 'zjzlWwFwPnZ4zO4Qsif5f64cOu7WfV7riYBm9Aq+VpxXOL8R4rEOhVmt\
3xDrKcDvtA7+GfSOt46MkUPGKqzmI5P/+e1wRtHfTWO5bPQ54mxaUnvba4Oj142SEBq4Nbj\
SO5zBXrILFY+CFtIp1Y3Cq5G3A2BhljqWVWifLHQe51uIx+OuJJ2mEUzRne3ONHOwoV5sWE9\
CEQzDdAlo1AxjYEkC3VurCwz4ywQKUQ6ccw9hVLksizn+fm0WCVVCW3vs'

sandboxCookie = '13313047145.5774'

if __name__ == "__main__":
    ret = []
    res = requests.post('https://mediaweb.ap.panopto.com/Panopto/Services/Data.svc/GetSessions', headers={
        'cookie': f'.ASPXAUTH={ASPXAUTH}; sandboxCookie={sandboxCookie}'}, json=parameters)
    if res.status_code != 200:
        print('cookie & auth wrong or expired, reset them')
        exit(1)
    r = res.json()
    if r['d']['Results'] is None or len(r['d']['Results']) == 0:
        print('no results, check your cookie and auth')
        exit(1)
    for i in r['d']['Results']:
        ret.append((i['SessionName'], i['IosVideoUrl']))
