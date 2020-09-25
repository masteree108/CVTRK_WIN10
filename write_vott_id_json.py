import os, shutil
import json
import hashlib
# pip install shortuuid
import shortuuid

class write_vott_id_json():
# private
    def __clear_all_parameter_value(self):
        self.asset_id = ""
        self.asset_format = ""
        self.asset_path = ""

        self.parent_id = ""
        self.parent_name = ""
        self.parent_path = ""

        self.video_size = [3840, 2160]
        self.timestamp = 0
        
        self.regions_id = ""
        self.tags = ""
        self.boundingBox = []
        self.points = []
    def __save_asset_id(self, sid):
        self.asset_id = sid

    def __save_regions_id(self, rid):
        self.regions_id = rid

    def __create_asset_id_via_md5(self, path):
        m = hashlib.md5()
        m.update(path.encode("utf-8"))
        h = m.hexdigest()
        print("asset_id: %s" % h)
        self.__save_asset_id(h)

    def __create_shorid_for_regions_id(self):
        sid = shortuuid.uuid()
        sid = sid[:9]
        self.__save_regions_id(sid)

# public
    def __init__(self, target_path):
        self.target_path = ""
        if os.path.exists(target_path):
            self.target_path = target_path
            #print("target_path: %s" % target_path)
        else:
            print('target path is not existed!!')
        self.__clear_all_parameter_value()
    
    def create_id_json_file(self, json_file_path):
        try:
            self.__create_shorid_for_regions_id()
            new_json_file_path = self.target_path + self.asset_id + '-asset.json'
            print(new_json_file_path)
            shutil.copyfile(json_file_path, new_json_file_path); 
            with open( new_json_file_path, 'r+') as f:
                data = json.load(f)
                data['asset']['id'] = self.asset_id
                data['asset']['format'] = self.asset_format 
                data['asset']['name'] = self.asset_name
                data['asset']['path'] = self.asset_path
 
                #data['asset']['parent']['id'] = self.parent_id
                #data['asset']['parent']['name'] = self.parent_name
                #data['asset']['parent']['path'] = self.parent_path
 
                data['asset']['timestamp'] = self.timestamp
                data['regions'][0]['id'] = self.regions_id
                data['regions'][0]['tags'][0] = self.tags
                data['regions'][0]['boundingBox']["height"] = self.boundingBox[0]
                data['regions'][0]['boundingBox']["width"] = self.boundingBox[1]
                data['regions'][0]['boundingBox']["left"] = self.boundingBox[2]
                data['regions'][0]['boundingBox']["top"] = self.boundingBox[3]

                data['regions'][0]['points'][0]["x"] = self.boundingBox[2]
                data['regions'][0]['points'][0]["y"] = self.boundingBox[3]
                
                data['regions'][0]['points'][1]["x"] = self.points[0]
                data['regions'][0]['points'][1]["y"] = self.boundingBox[3]
                
                data['regions'][0]['points'][2]["x"] = self.points[0]
                data['regions'][0]['points'][2]["y"] = self.points[1]
                
                data['regions'][0]['points'][3]["x"] = self.boundingBox[2]
                data['regions'][0]['points'][3]["y"] = self.points[1]

                f.close()
            os.remove(new_json_file_path)

            with open( new_json_file_path, 'w') as f:
                json.dump(data, f, indent = 4)
                f.close()

            return False
        except:
            print(' write vott id json failed ')
            return True

    
    def save_asset_format(self, sformat):
        self.asset_format = sformat
    
    def save_asset_name(self, sname):
        self.asset_name = sname

    def save_asset_path(self, spath):
        self.asset_path = spath
        self.__create_asset_id_via_md5(self.asset_path)

    def save_parent_id(self, pid):
        self.parent_id = pid

    def save_parent_name(self, pname):
        self.parent_name = pname

    def save_parent_path(self, ppath):
        self.parent_path = ppath

    def save_video_size(self, size):
        self.video_size = size

    def save_timestamp(self, timestamp):
        self.timestamp = timestamp
    
    def save_tags(self, tags):
        self.tags = tags

    def save_boundingBox(self, BX):
        self.boundingBox = []
        self.boundingBox.append(BX[0])  #height 
        self.boundingBox.append(BX[1])  #width 
        self.boundingBox.append(BX[2])  #left
        self.boundingBox.append(BX[3])  #top
    
    def save_points(self, PT):
        #self.points.append(PT[0])  #x1 = left
        #self.points.append(PT[1])  #y1 = top
        self.points = []
        self.points.append(PT[0])  #x2
        self.points.append(PT[1])  #y2

