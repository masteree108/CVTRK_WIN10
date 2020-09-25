import os
import json

class read_vott_id_json():
# private
    def __clear_all_parameter_value(self):
        self.asset_id = ""
        self.asset_format = ""
        self.asset_name = ""
        self.asset_path = ""
        self.video_size = [3840, 2160]

        self.parent_id = ""
        self.parent_name = ""

        self.timestamp = 0
        self.tags = ""
        self.regions_id = ""
        self.boundingBox = [0,0,0,0]

    def __print_read_parameter_from_json(self):
        print("asset_id: %s" % self.asset_id)
        print("asset_format: %s" % self.asset_format)
        print("asset_name: %s" % self.asset_name)
        print("asset_path: %s" % self.asset_path)
        print("width: %d" % self.video_size[0])
        print("height: %d" % self.video_size[1])

        print("parent_id: %s" % self.parent_id)
        print("parent_name: %s" % self.parent_name)
        print("parent_path: %s" % self.parent_path)

        print("timestamp: %.5f" % self.timestamp)
        print("tags: %s" % self.tags)
        print("boundingBox height: %s" % self.boundingBox[0])
        print("boundingBox width: %s" % self.boundingBox[1])
        print("boundingBox left: %s" % self.boundingBox[2])
        print("boundingBox top: %s" % self.boundingBox[3])


# public
    def __init__(self, file_path):
        self.file_path = ""
        if os.path.exists(file_path):
            self.file_path = file_path
            self.__clear_all_parameter_value()
            print("file_path: %s" % file_path)
        else:
            print('file is not existed!!')
    
    def read_from_id_json_data(self):
        try:
            with open(self.file_path, 'r') as reader:
                print("open_ok")
                jf = json.loads(reader.read())
                self.asset_id = jf['asset']['id']
                self.asset_format = jf['asset']['format']
                self.asset_name = jf['asset']['name']
                self.asset_path = jf['asset']['path']
                self.video_size[0] = jf['asset']['size']['width']
                self.video_size[1] = jf['asset']['size']['height']
                self.timestamp = jf['asset']['timestamp']

                self.parent_id = jf['asset']['parent']['id']
                self.parent_name = jf['asset']['parent']['name']
                self.parent_path = jf['asset']['parent']['path']

                self.tags = jf['regions'][0]['tags'][0]
                self.boundingBox[0] = jf['regions'][0]['boundingBox']["height"]
                self.boundingBox[1] = jf['regions'][0]['boundingBox']["width"]
                self.boundingBox[2] = jf['regions'][0]['boundingBox']["left"]
                self.boundingBox[3] = jf['regions'][0]['boundingBox']["top"]
                print("read form json ok")
                self.__print_read_parameter_from_json()
                reader.close() 
            return False
        except:
            print(' wrong format: '+ self.file_path)
            return True

    def get_asset_id(self):
        return self.asset_id
    
    def get_asset_format(self):
        return self.asset_format
    
    def get_asset_name(self):
        return self.asset_name

    def get_asset_path(self):
        return self.asset_path

    def get_parent_id(self):
        return self.parent_id
    
    def get_parent_name(self):
        return self.parent_name
    
    def get_parent_path(self):
        return self.parent_path

    def get_video_size(self):
        return self.video_size

    def get_timestamp(self):
        return self.timestamp
    
    def get_tags(self):
        return self.tags

    def get_boundingBox(self):
        BX = [0,0,0,0]
        BX[0] = self.boundingBox[2]     #x1=left
        BX[1] = self.boundingBox[3]     #y1=top    
        BX[2] = self.boundingBox[1]     #x2=width    
        BX[3] = self.boundingBox[0]     #y2=height 
        return BX

