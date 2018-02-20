# -*- coding: utf-8 -*-
import json
import requests
import traceback


class TulingAutoReply:
    def __init__(self, tuling_key, tuling_url):
        self.key = tuling_key
        self.url = tuling_url

    def reply(self, unicode_str):
        body = {'key': self.key, 'info': unicode_str.encode('utf-8')}
        r = requests.post(self.url, data=body)
        r.encoding = 'utf-8'
        resp = r.text
        if resp is None or len(resp) == 0:
            return None
        try:
            js = json.loads(resp)
            if js['code'] == 100000:
                return js['text'].replace('<br>', '\n')
            elif js['code'] == 200000:
                return js['url']
            else:
                return None
        except Exception:
            traceback.print_exc()
            return None

class GoogleVision_AutoReply:
    def __init__(self, google_vis_key, google_vis_url):
        self.key = google_vis_key
        self.url = google_vis_key
        
    def analyse(self, picture_url, picture_mediaID):
        parameters_pic_raw = {
            "requests":[
                {
                    "image":{
                        "source":{
                            "imageUri":
                                picture_url
                        }
                    },
                     "features": [
                            {
                                "type": "FACE_DETECTION",
                                "maxResults": "10"
                            },
                            {
                                "type": "LABEL_DETECTION",
                                 "maxResults": "10"
                            },
                            {
                                "type": "TEXT_DETECTION",
                                "maxResults": "10"
                            },
                            {
                                "type": "LANDMARK_DETECTION",
                                "maxResults": "10"
                            },
                            {
                                "type": "WEB_DETECTION",
                                "maxResults": "10"
                            }
                     ]
                }
            ]
        }
        
        output_filename = 'vision_%s.json'%picture_mediaID
        with open(output_filename, 'w') as output_file:
            json.dump(parameters_pic_raw, output_file, indent = 4)
        
        parameters_pic = open(output_filename,'rb').read()
        response_pic = requests.post(url = self.url + '?key=' + self.key, data = parameters_pic)
        
        vision_results = response_pic.json()
        
        return vision_results


class DefaultAutoReply:
    def __init__(self):
        pass

    def reply(self, unicode_str):
        return None
