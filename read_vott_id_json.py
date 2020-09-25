import os
import sys
import json
import enum
import log as PYM

class BBOX_ITEM(enum.Enum):
    height = 0
    width = 1
    left = 2
    top = 3

class VIDEO_SIZE(enum.Enum):
    W = 0
    H = 1

class read_vott_id_json():
# private
    __asset_id = ""
    __asset_format = ""
    __asset_name = ""
    __asset_path = ""
    __video_size = [3840, 2160]

    __parent_id = ""
    __parent_name = ""

    __timestamp = 0
    __tags = ""
    __regions_id = ""
    __boundingBox = [0,0,0,0]

    def __print_read_parameter_from_json(self):
        self.pym.PY_LOG(False, 'D', self.__class__, 'asset_id: %s' % self.__asset_id)
        self.pym.PY_LOG(False, 'D', self.__class__, 'asset_format: %s' % self.__asset_format)
        self.pym.PY_LOG(False, 'D', self.__class__, 'asset_name: %s' % self.__asset_name)
        self.pym.PY_LOG(False, 'D', self.__class__, 'asset_path %s' % self.__asset_path)
        self.pym.PY_LOG(False, 'D', self.__class__, 'video_width: %d' % self.__video_size[VIDEO_SIZE.W.value])
        self.pym.PY_LOG(False, 'D', self.__class__, 'video_height: %d' % self.__video_size[VIDEO_SIZE.H.value])

        self.pym.PY_LOG(False, 'D', self.__class__, 'parent_id: %s' % self.__parent_id)
        self.pym.PY_LOG(False, 'D', self.__class__, 'parent_name: %s' % self.__parent_name)
        self.pym.PY_LOG(False, 'D', self.__class__, 'parent_path: %s' % self.__parent_path)

        self.pym.PY_LOG(False, 'D', self.__class__, 'timestamp: %.5f' % self.__timestamp)
        self.pym.PY_LOG(False, 'D', self.__class__, 'tags: %s' % self.__tags)
        self.pym.PY_LOG(False, 'D', self.__class__, 'bounding box height: %s' % self.__boundingBox[BBOX_ITEM.height.value])
        self.pym.PY_LOG(False, 'D', self.__class__, 'bounding box width: %s' % self.__boundingBox[BBOX_ITEM.width.value])
        self.pym.PY_LOG(False, 'D', self.__class__, 'bounding box left: %s' % self.__boundingBox[BBOX_ITEM.left.value])
        self.pym.PY_LOG(False, 'D', self.__class__, 'bounding box top: %s' % self.__boundingBox[BBOX_ITEM.top.value])


# public
    def __init__(self, file_path):
        # below(True) = exports log.txt
        self.pym = PYM.LOG(True)
        self.file_path = ""
        if os.path.exists(file_path):
            self.file_path = file_path
            self.pym.PY_LOG(False, 'D', self.__class__, '%s existed!' % file_path)
        else:
            self.pym.PY_LOG(False, 'E', self.__class__, '%s is not existed!' % file_path)

    #del __del__(self):
        #deconstructor 

    def read_from_id_json_data(self):
        try:
            with open(self.file_path, 'r') as reader:
                self.pym.PY_LOG(False, 'D', self.__class__, '%s open ok!' % self.file_path)
                jf = json.loads(reader.read())
                self.__asset_id = jf['asset']['id']
                self.__asset_format = jf['asset']['format']
                self.__asset_name = jf['asset']['name']
                self.__asset_path = jf['asset']['path']
                self.__video_size[VIDEO_SIZE.W.value] = jf['asset']['size']['width']
                self.__video_size[VIDEO_SIZE.H.value] = jf['asset']['size']['height']
                self.__timestamp = jf['asset']['timestamp']

                self.__parent_id = jf['asset']['parent']['id']
                self.__parent_name = jf['asset']['parent']['name']
                self.__parent_path = jf['asset']['parent']['path']

                self.__tags = jf['regions'][0]['tags'][0]
                self.__boundingBox[BBOX_ITEM.height.value] = jf['regions'][0]['boundingBox']["height"]
                self.__boundingBox[BBOX_ITEM.width.value] = jf['regions'][0]['boundingBox']["width"]
                self.__boundingBox[BBOX_ITEM.left.value] = jf['regions'][0]['boundingBox']["left"]
                self.__boundingBox[BBOX_ITEM.top.value] = jf['regions'][0]['boundingBox']["top"]
                self.pym.PY_LOG(False, 'D', self.__class__, '%s read ok!' % self.file_path)
                self.__print_read_parameter_from_json()
                reader.close() 
        except:
            self.pym.PY_LOG(False, 'E', self.__class__, '%s has wrong format!' % self.file_path)
            sys.exit()

    def get_asset_id(self):
        return self.__asset_id
    
    def get_asset_format(self):
        return self.__asset_format
    
    def get_asset_name(self):
        return self.__asset_name

    def get_asset_path(self):
        return self.__asset_path

    def get_parent_id(self):
        return self.__parent_id
    
    def get_parent_name(self):
        return self.__parent_name
    
    def get_parent_path(self):
        return self.__parent_path

    def get_video_size(self):
        return self.__video_size

    def get_timestamp(self):
        return self.__timestamp
    
    def get_tags(self):
        return self.__tags

    def get_boundingBox(self):
        BX = [0,0,0,0]
        BX[0] = self.__boundingBox[BBOX_ITEM.left.value]     #x1=left
        BX[1] = self.__boundingBox[BBOX_ITEM.top.value]     #y1=top    
        BX[2] = self.__boundingBox[BBOX_ITEM.width.value]     #x2=width    
        BX[3] = self.__boundingBox[BBOX_ITEM.height.value]     #y2=height 
        return BX

    def shut_down_log(self, msg):
        self.pym.PY_LOG(True, 'D', self.__class__, msg)
