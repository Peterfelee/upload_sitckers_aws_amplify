import json

import requests

if __name__ == '__main__':
    key = '27666042-b7415ad41be674a8befb29fb4'
    pix_pthoto_url = f"https://pixabay.com/api/?key={key}&q=yellow+flowers&image_type=photo"
    pix_video_url = f"https://pixabay.com/api/videos/?key={key}&q=yellow+flowers"

    for index in range(0,10):
        response = requests.post(pix_pthoto_url)
        str = response.content
        dict = json.loads(str)
        print(f"\n{dict}")

