# coding=utf-8

import base64
import json

from .youkujs import *
from ..extractor import VideoExtractor
from ..common import *

class Acorig(VideoExtractor):
    name = u"AcFun 优酷合作视频"

    client_id = '908a519d032263f8'
    ct = 85
    refer = 'http://cdn.aixifan.com/player/sslhomura/AcFunV3Player170213.swf'
    key = "2da3ca9e"

    stream_types = [
        {'id': 'TD', 'container': 'mp4', 'video_profile': '超清'},
        {'id': 'HD', 'container': 'mp4', 'video_profile': '高清'},
        {'id': 'SD', 'container': 'mp4', 'video_profile': '标清'},
    ]

    def __init__(self, *args):
        super(Acorig, self).__init__(*args)
        self.embsig = None

    def prepare(self, **kwargs):
        self.embsig = kwargs['embsig']
        self.title = kwargs['title']

        api = "http://aauth-vod.cn-beijing.aliyuncs.com/acfun/web?vid={}&ct={}&time={}&ev=2".format(self.vid, self.ct,int(time.time()*1000))
        data = rc4(self.key, base64.b64decode(json.loads(get_content(api))['data']))
        stream_data = json.loads(data)
        for s in stream_data['stream']:
            if 'segs' in s:
                stream_type = stream_code_to_id[s['stream_type']]
                stream_urls = [seg['url'] for seg in s['segs']]
                size = s['size']
                self.streams[stream_type] = {'container': 'mp4', 'video_profile': stream_code_to_profiles[stream_type], 'src': stream_urls, 'size' : size}

        print (self.streams)

"""
self.streams[stream_id] = {
        'container': stream_types[stream_id]['container'],
        'video_profile': stream_types[stream_id]['video_profile'],
        'size': stream['size'],
        'pieces': [{
            'fileid': stream['stream_fileid'],
            'segs': stream['segs']
        }]
    }
"""