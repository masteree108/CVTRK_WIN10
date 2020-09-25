import os
import sys
import read_vott_id_json as RVIJ
import write_vott_id_json as WVIJ
import cv_tracker as CVTR 
import log as PYM
from threading import Timer

ROI_get_bbox = False 
py_name = 'vott_tracker' 

def fill_previous_data_to_write_json(rvij, wvij):
    
    wvij.save_parent_id(rvij.get_parent_id())
    wvij.save_parent_name(rvij.get_parent_name())
    wvij.save_parent_path(rvij.get_parent_path())
    
    wvij.save_tags(rvij.get_tags())

    pym.PY_LOG(False, 'D', py_name , 'fill previous data ok')

  
def deal_with_name_format_path(rvij, wvij, now_frame_timestamp_DP, now_format): 
    
    pym.PY_LOG(False, 'D', py_name, 'now_frame_timestamp_DP: %.5f' % now_frame_timestamp_DP)
    pym.PY_LOG(False, 'D', py_name, 'now_fromat: %s' % now_format)
    org_asset_name = rvij.get_asset_name()
    org_timestamp = rvij.get_timestamp()
    org_asset_path = rvij.get_asset_path()
    pym.PY_LOG(False, 'D', py_name, 'org_asset_name: %s' % org_asset_name)
    pym.PY_LOG(False, 'D', py_name, 'org_timestamp: %.5f' % org_timestamp)
    pym.PY_LOG(False, 'D', py_name, 'org_asset_path: %s' % org_asset_path)
    
    org_timestamp = int(org_timestamp)
    
    name_count = org_asset_name.find('=')
    org_asset_name = org_asset_name[:name_count+1]
    now_timestamp = now_frame_timestamp_DP
    now_timestamp = str(org_timestamp +  now_timestamp)
    now_asset_name = org_asset_name + now_timestamp
    pym.PY_LOG(False, 'D', py_name, 'now_frame_asset_name: %s' % now_asset_name)
    pym.PY_LOG(False, 'D', py_name, 'now_timestamp: %s' % now_timestamp)
    
    path_count = org_asset_path.find('=')
    org_asset_path = org_asset_path[:path_count+1]     
    now_asset_path = org_asset_path + now_timestamp
    pym.PY_LOG(False,'D', py_name, 'now_frame_asset_path: %s' % now_asset_path)

    #this function will be created id via path by md5 method 
    wvij.save_asset_path(now_asset_path)
    wvij.save_asset_format(now_format)
    wvij.save_asset_name(now_asset_name)
    wvij.save_timestamp(now_timestamp)


def deal_with_BX_PT(wvij, bbox): 
    BX = []
    BX.append(bbox[3])  #height BX[0]
    BX.append(bbox[2])  #width BX[1]
    BX.append(bbox[0])  #left BX[2]
    BX.append(bbox[1])  #top BX[3]

    wvij.save_boundingBox(BX)

    PT =[]
    PT.append(BX[1]+BX[2])
    PT.append(BX[0]+BX[3])
    wvij.save_points(PT)

def timer_isr():
    global arrived_next_frame 
    arrived_next_frame = True

class RepeatingTimer(Timer): 
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)

def main(target_path, json_file_path, video_path, algorithm):
    
    # get video's time that VoTT user to label track object 
    timestamp = 0

    # get bounding box position
    bbox = ()
    rvij = RVIJ.read_vott_id_json(json_file_path)
    rvij.read_from_id_json_data()

    timestamp = rvij.get_timestamp()
    get_bbox = rvij.get_boundingBox()
    bbox = (get_bbox[0], get_bbox[1], get_bbox[2],  get_bbox[3])
    
    
    # VoTT cv tracker settings
    # debug mode
    # pos0: show video with bbox             
    # pos1: save image with bbox             
    # pos2: save viedo with bbox     
    # ROI_get_bbox just a tester to test tracking function
    image_debug = [1, 0, 0]
    cvtr = CVTR.CV_TRACKER(algorithm, video_path, timestamp, bbox, image_debug, ROI_get_bbox)

    vott_video_fps = 15
    frame_count = cvtr.get_label_frame_number(rvij.get_asset_format(), vott_video_fps)
    if frame_count == 14:
        pym.PY_LOG(False, 'W', py_name, 'this is the last frame at this second, so exit auto tracking!!')
        sys.exit()

    pym.PY_LOG(False, 'D', py_name, 'user to label frame number: %d' % frame_count)

    # about write data to json file  
    wvij = WVIJ.write_vott_id_json(target_path)
    fill_previous_data_to_write_json(rvij, wvij)


    # timer setting
    frame_interval = cvtr.get_frame_interval_for_timer_count(vott_video_fps)
    timer = RepeatingTimer(frame_interval, timer_isr)
    timer.start()

    global arrived_next_frame
    while True:
        frame = cvtr.capture_video_frame()
        if arrived_next_frame:
            bbox = cvtr.draw_boundbing_box_and_get(frame)
            frame_count = frame_count + 1
            
            now_frame_timestamp_DP = cvtr.get_now_frame_timestamp_DP(frame_count, vott_video_fps)
            now_format = cvtr.get_now_format_value(frame_count, vott_video_fps)
            
            deal_with_name_format_path(rvij, wvij, now_frame_timestamp_DP, now_format)
            deal_with_BX_PT(wvij, bbox) 
            pym.PY_LOG(False, 'D', py_name, 'frame_count: %d' % frame_count)
            wvij.create_id_json_file(json_file_path)
            arrived_next_frame = False 
        cvtr.use_waitKey(1)
        if frame_count == 14:
            timer.cancel()
            #shut_down log
            pym.PY_LOG(True, 'D', py_name, '__done___')
            rvij.shut_down_log('__done__')
            wvij.shut_down_log('__done__')
            cvtr.shut_down_log('__done__\n\n\n\n')
            break

def read_file_name_path(target_path):
    #file ex:
    # file:/home/ivan/HD1/hd/VoTT/Drone_Project/Drone_Source/001/Drone_001.mp4#t=305.533333,76a8e999e2d9232d8e26253551acb4b3-asset.json

    if os.path.exists(target_path):
        pym.PY_LOG(False, 'D', py_name, 'target_path: %s existed!' % target_path)                                                                         
    else:
        pym.PY_LOG(False, 'E', py_name, 'target_path: %s is not existed!' % target_path)
        sys.exit()

    f = open(target_path, "r") 
    # remove file:
    path = f.read()
    path = path[5:]
    vc = 0
    
    # get source video path
    vc = path.find('#')
    video_path = path[:vc]
    pym.PY_LOG(False, 'D', py_name, 'video_path: %s' % video_path)

    # get json file(this file will be crated when user used vott to label object)
    vc = path.find(',')
    file_name = path[vc+1:]
    pym.PY_LOG(False, 'D', py_name, 'file_name: %s' % file_name)
    
    # replace Dorne_Source to Drone_Target because from video path,
    # because we need to get the json file at Drone_Target/target_name folder
    # please note if users target_name(ex:001) folder is not equal to source_name(ex:001) 
    # below target_path will be wrong!!!
    target_path = video_path.replace("Drone_Source", "Drone_Target")
    l1 = target_path.find("Drone_Target")
    l2 = l1 + len("Drone_Target/")
    temp_path = target_path[l2:]
    l3 = temp_path.find('/')
    last_dir_path = temp_path[:l3] 
    target_path = target_path[:l2] + last_dir_path + '/'
    pym.PY_LOG(False, 'D', py_name, 'target_path: %s' % target_path)
    json_file_path = target_path + file_name
    pym.PY_LOG(False, 'D', py_name, 'json_file_path: %s' % json_file_path)
    return video_path, target_path, json_file_path



if __name__ == '__main__':
    # below(True) = exports log.txt
    pym = PYM.LOG(True)  

    target_path = '../../Drone_Project/Drone_Target/for_python_path.log'
    video_path, target_path, json_file_path = read_file_name_path(target_path)
    #if len(sys.argv[1]) > 1:
        #file_path = file_path + sys.argv[1]
        #print("file_path: %s" % file_path)
    #if len(sys.argv[2]) > 1:
        #algorithm = sys.argv[2]
        #print(algorithm)

    arrived_next_frame = False 
    algorithm = 'CSRT'
    main(target_path, json_file_path, video_path, algorithm)
