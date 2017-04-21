#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['meipai_download']

import base64
from ..common import *

def meipai_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    assert re.match(r'http://[^\.]+.meipai.[^\.]+/media/(\d+)', url)
    html = get_html(url)

    title = r1(r'<h1[^>]+>([\s\S]+)</h1>', html)
    title = unescape_html(title)
    title = escape_file_path(title)
    title = title.strip()
    assert title

    video_encoded_url = r1(r'data-video="([^"]+)"', html)
    assert video_encoded_url

    video_decoded_url = MeipaiDecoder().decode(video_encoded_url)
    assert video_decoded_url

    if isinstance(video_decoded_url, bytes):
        video_decoded_url = video_decoded_url.decode()

    type, ext, size = url_info(str(video_decoded_url))

    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([video_decoded_url], title, ext, size, output_dir, merge = merge)

class MeipaiDecoder(object):
    def getHex(self, src):
        """"""
        """
        return {
            "str":param1[SUB_STRING](4),
            "hex":param1[SUB_STRING](0,4)[SPLIT]("").reverse().join("")
         };
        """
        return {
            "str": src[4:],
            "hex": ''.join(reversed(src[:4])),
        }

    def getDec(self, src):
        """"""
        """
        var _loc2_:String = parseInt(param1,16).toString();
         return {
            "pre":_loc2_[SUB_STRING](0,2)[SPLIT](""),
            "tail":_loc2_[SUB_STRING](2)[SPLIT]("")
         };
        """
        l = str(int(src, 16))
        return {
            'pre': l[:2],
            'tail': l[2:],
        }

    def substr(self, param1, param2):
        """"""
        """
        var _loc3_:String = param1[SUB_STRING](0,param2[0]);
         var _loc4_:String = param1[SUB_STR](param2[0],param2[1]);
         return _loc3_ + param1[SUB_STRING](param2[0])[REPLACE](_loc4_,"");
        """
        param2 = [int(l) for l in param2]
        l1 = param1[0:param2[0]]
        l2 = param1[param2[0]:param2[0] + param2[1]]
        return l1 + param1[param2[0]:].replace(l2, '')

    def getPos(self, param1, param2):
        """"""
        """
        param2[0] = param1.length - param2[0] - param2[1];
         return param2;
        """
        param2 = [int(l) for l in param2]
        param2[0] = len(param1) - param2[0] - param2[1]
        return param2

    def decode(self, param1):
        """"""
        """
        var _loc2_:Object = getHex(param1);
         var _loc3_:Object = getDec(_loc2_.hex);
         var _loc4_:String = substr(_loc2_.str,_loc3_.pre);
         return Base64.decode(substr(_loc4_,getPos(_loc4_,_loc3_.tail)));
        """
        l1 = self.getHex(param1)
        l2 = self.getDec(l1['hex'])
        l3 = self.substr(l1['str'], l2['pre'])
        pos = self.getPos(l3, l2['tail'])
        v = self.substr(l3, pos)
        return base64.b64decode(v)


site_info = "Meipai.com"
download = meipai_download
download_playlist = playlist_not_supported("baidu")