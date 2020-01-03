from http.server import BaseHTTPRequestHandler
import requests
import json
from PIL import Image
from io import BytesIO

class handler(BaseHTTPRequestHandler):
    def getContributors(self, org, repo):
        response = requests.get(f'https://api.github.com/repos/{org}/{repo}/contributors')
        contributors = json.load(response)
        images = []

        new_im = Image.new('RGB', (total_width, max_height))

        for contributor in contributors:
            avatar_url = contributor["avatar_url"]
            stream_img = requests.get(avatar_url)
            images.append(Image.open(BytesIO(response.content)))


        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset,0))
            x_offset += im.size[0]

        