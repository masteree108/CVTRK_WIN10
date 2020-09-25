import cv2
import sys
import enum
import log as PYM


class IMAGE_DEBUG(enum.Enum):
    # SW_VWB: show video with bbox 
    SW_VWB = 0
    # SE_IWB: save image with bbox 
    SE_IWB  = 1
    # SIWB: save viedo with bbox 
    SE_VWB  = 2
    

class CV_TRACKER():
# private
    # unit: second ,DP=Decimal point
    __frame_timestamp_DP_15fps = [0, 0.066667, 0.133333, 0.2, 0.266667, 0.333333,
                       0.4, 0.466667, 0.533333, 0.6, 0.666667, 0.733333,
                       0.8, 0.866667, 0.933333]

    __format_15fps = ['mp4', '066667', '133333', '2', '266667', '333333',
                       '4', '466667', '533333', '6', '666667', '733333',
                       '8', '866667', '933333']
    
    # if there is needing another format fps please adding here

    __video_cap = 0
    __tracker = 0
    __image_debug = [0,0,0,0]
       
    def __get_algorithm_tracker(self, algorithm):
        
        if algorithm == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        elif algorithm == 'MIL':  
            tracker = cv2.TrackerMIL_create()
        elif algorithm == 'KCF':  
            tracker = cv2.TrackerKCF_create()
        elif algorithm == 'TLD':  
            tracker = cv2.TrackerTLD_create()
        elif algorithm == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        elif algorithm == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        elif algorithm == 'CSRT':                       
            tracker = cv2.TrackerCSRT_create()
        elif algorithm == 'MOSSE':                                                                                          
            tracker = cv2.TrackerMOSSE_create()
        else: 
            #default settings
            tracker = cv2.TrackerCSRT_create()
        return tracker

    def __check_which_frame_number(self, format_value, format_fps):
        for count in range(len(format_fps)):
            if format_value == format_fps[count]:
                return count
    
    def __show_video_with_bounding_box(self, window_name ,frame, wk_value):
        cv2.imshow(window_name, frame)
        cv2.waitKey(wk_value)

# public
    def __init__(self, algorithm, video_path, label_object_time_in_video, bbox, image_debug, ROI_get_bbox):
        # below(True) = exports log.txt
        self.pym = PYM.LOG(True)      

        # 1. make sure video is existed
        self.__video_cap = cv2.VideoCapture(video_path)
        if not self.__video_cap.isOpened():
            self.pym.PY_LOG(False, 'E', self.__class__, 'open video failed!!.')
            sys.exit() 
        
        # 2. reading video strat time at the time that user using VoTT to label trakc object
        # *1000 because CAP_PROP_POS_MESE is millisecond
        self.__video_cap.set(cv2.CAP_PROP_POS_MSEC, label_object_time_in_video*1000)                              
        # ex: start time at 50s
        #self.video_cap.set(cv2.CAP_PROP_POS_MSEC, 50000)
        #self.video_cap.set(cv2.CAP_PROP_FPS, 15)  #set fps to change video,but not working!!

        # 3. setting tracker algorithm and init
        self.__tracker =  self.__get_algorithm_tracker(algorithm) 
        self.pym.PY_LOG(False, 'D', self.__class__, 'VoTT_CV_TRACKER initial ok')
        frame = self.capture_video_frame()

        if ROI_get_bbox:
           bbox = self.use_ROI_select('ROI_select', frame)

        self.__tracker.init(frame, bbox)
        self.pym.PY_LOG(False, 'D', self.__class__, 'openCV tracker initial ok')
    
        # 4. for debuging
        self.__image_debug[IMAGE_DEBUG.SW_VWB.value] = image_debug[0]
        self.__image_debug[IMAGE_DEBUG.SE_IWB.value] = image_debug[1]
        self.__image_debug[IMAGE_DEBUG.SE_VWB.value] = image_debug[2]
        if self.__image_debug[IMAGE_DEBUG.SW_VWB.value] == 1 or \
           self.__image_debug[IMAGE_DEBUG.SE_IWB.value] == 1 or \
           self.__image_debug[IMAGE_DEBUG.SE_VWB.value] == 1 :
            self.window_name = 'debug'
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)                                                   
            cv2.resizeWindow(self.window_name, 1280, 720)

        # 5. just show video format information
        self.show_video_format_info()
        
        self.pym.PY_LOG(False, 'D', self.__class__, 'VoTT_CV_TRACKER initial ok')

    #del __del__(self):
        #deconstructor     

    def capture_video_frame(self):
        ok, frame = self.__video_cap.read()
        if not ok:
            self.pym.PY_LOG(False, 'E', self.__class__, 'open video failed!!')
            sys.exit()
        #try:                           
        #    frame = cv2.resize(frame, (1280, 720))                                                                         
        #except:      
        #   self.pym.PY_LOG(False, 'E', "frame resize failed!!")
        return frame

    
    def get_label_frame_number(self, format_value, fps):
        # check which frame that user use VoTT tool to label
        if fps == 15:
            return self.__check_which_frame_number(format_value, self.__format_15fps)
        # for adding new fps format use, please write it here
        #elif fps == 30:
            #return self.__check_which_frame_number(format, self.__format_30fps)
        else:
            self.pym.PY_LOG(False, 'W', self.__class__, 'This version only provides 15fps format check,\
            so use 15fps check to get label frame number')
            return self.__check_which_frame_number(format_value, self.__format_15fps)
    
    def get_now_format_value(self, frame_count, fps):
        # check which frame that user use VoTT tool to label
        if fps == 15:
            return self.__format_15fps[frame_count]
        # for adding new fps format use, please write it here
        #elif fps == 30:
            #return self.__format_30fps[frame_count]
        else:
            self.pym.PY_LOG(False, 'W', self.__class__, 'This version only provides 15fps format check,\
            so use 15fps check to get format value')
            return self.__format_15fps[frame_count]
   
    def use_ROI_select(self, ROI_window_name, frame):
        cv2.namedWindow(ROI_window_name, cv2.WINDOW_NORMAL)                                                   
        cv2.resizeWindow(ROI_window_name, 1280, 720)
        bbox = cv2.selectROI(ROI_window_name, frame, False)
        cv2.destroyWindow(ROI_window_name)
        return bbox

       
    def draw_boundbing_box_and_get(self, frame):
        ok, bbox = self.__tracker.update(frame)
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            # below rectangle last parament = return frame picture
            cv2.rectangle(frame, p1, p2, (255, 0 ,0 ), 2, 0)
        else:
            if self.image_debug[IMAGE_DEBUG.SW_VWB.value] == 1 or \
               self.image_debug[IMAGE_DEBUG.SE_IWB.value] == 1 or \
               self.image_debug[IMAGE_DEBUG.SE_VWB.value] == 1 :
                cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 3, 255), 2)
            else:
                self.pym.PY_LOG(False, 'W', self.__class__, 'Tarcking failre detected')
                

        if self.__image_debug[IMAGE_DEBUG.SW_VWB.value] == 1:
            # showing video with bounding box
            self.__show_video_with_bounding_box(self.window_name ,frame, 1)
         
        return bbox

    def use_waitKey(self, value):
        cv2.waitKey(value)

    def show_video_format_info(self):
        self.pym.PY_LOG(False, 'D', self.__class__, '===== source video format start =====')
        wid = int(self.__video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        hei = int(self.__video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_rate = int(self.__video_cap.get(cv2.CAP_PROP_FPS))
        frame_num = int(self.__video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.pym.PY_LOG(False, 'D', self.__class__, 'video width: %d' % wid)
        self.pym.PY_LOG(False, 'D', self.__class__, 'height: %d' % hei)
        
        # below framenum / framerate = video length
        self.pym.PY_LOG(False, 'D', self.__class__, 'framerate: %d' % frame_rate)
        self.pym.PY_LOG(False, 'D', self.__class__, 'framenum: %d' % frame_num)
        video_length = float(frame_num / frame_rate)
        self.pym.PY_LOG(False, 'D', self.__class__, 'video length: %.5f secs' % video_length)
        self.pym.PY_LOG(False, 'D', self.__class__, '===== source video format over =====')
    
    def get_now_frame_timestamp_DP(self, frame_count, fps):
        if fps == 15:
            return self.__frame_timestamp_DP_15fps[frame_count]
        #elif fps == 30: 
        #
        else:
            self.pym.PY_LOG(False, 'W', self.__class__, 'get_now_frame_time() fps parament is not correct, \
                                                    so use default settings(15fps)')
            return self.__frame_timestamp_DP_15fps[frame_count]
            
    def get_frame_interval_for_timer_count(self, fps):
        frame_interval = 0.1
        if fps == 15:
            # 1 sec(15 frames) interval = 1/15 = 0.066667
            frame_interval = 0.066667
            self.pym.PY_LOG(False, 'D', self.__class__, 'frame_interval: %.6f' % frame_interval)
        #elif fps == 30:
        #
        else:
            frame_interval = 0.066667
            self.pym.PY_LOG(False, 'W', self.__class__, 'get_frame_interval_for_timer_count() fps parament\
                                                    is not correct, so frame_interval use \
                                                    default setting = 0.066667')
        return float(frame_interval)
    
    def shut_down_log(self, msg):
        self.pym.PY_LOG(True, 'D', self.__class__, msg)




