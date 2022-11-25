from contextlib import closing
import requests, os

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
                print("\r %s [%s%s] %d%% " % (video_name+"---->", done_block * '█', ' ' * (50 - 1 - done_block), current_progress), end=" ")


if __name__ == '__main__':
    url = "https://s-cloudfront.cdn.ap.panopto.com/sessions/e4497797-1e79-4eb4-bd77-aee5006115c9/567aa836-bdab-4c1f-87b4-aee5006115cf-3cbe42be-22df-4cef-8909-af46007e7d59.mp4"
    video_path = "测试.mp4"

    download_video(url, video_path)
