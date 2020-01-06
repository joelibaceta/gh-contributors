from http.server import BaseHTTPRequestHandler
import requests
import json
import re
import math
from PIL import Image
from io import BytesIO

class handler(BaseHTTPRequestHandler):

    def get_param(self, name, path, default=None):
        pattern = re.compile(r""+name+"\=([^\=\&]+)")
        match = pattern.search(path)
        if match is not None:
            return match.group(1)
        else:
            return default

    def do_GET(self):
        org = self.get_param('org', self.path)
        repo = self.get_param('repo', self.path)
        print(org)
        print(repo)
        output = BytesIO()
        image = self.getContributors(org, repo)
        image.save(output)

        self.send_response(200)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Disposition", "attachment")
        self.send_header("Content-type", "image/jpeg")
        self.end_headers()
        self.wfile.write(output)
        return  

    def getContributors(self, org, repo):

        response = requests.get(f'https://api.github.com/repos/{org}/{repo}/contributors')
        contributors = response.json()
        images = []

        for contributor in contributors:
            avatar_url = contributor["avatar_url"]
            stream_img = requests.get(avatar_url)
            images.append(Image.open(BytesIO(stream_img.content)))

        rows = math.ceil(len(images) / 6)
        spacing = 2 * len(images) - 4
        new_im = Image.new('RGB', (6*64 + spacing, rows*64  + spacing-8), (255, 255, 255))
        x_offset, y_offset = 0, 0
        counter = 1

        for im in images:
            im2 = im.resize((64, 64))
            new_im.paste(im2, (x_offset, y_offset))
            if (counter % 6 == 0):
                y_offset += 2 + im2.size[0]
                x_offset = 0
            else:
                x_offset += 2 + im2.size[0]
            counter += 1

        return new_im