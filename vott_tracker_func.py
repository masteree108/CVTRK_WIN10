import json
import sys
import os
from tkinter import *                                                                                                                                                  
from tkinter import messagebox

py_name = '< vott_tracker_func >'
# for hinding tk window and changing position
root = Tk() 
root.geometry(f"10x10+80+50")

def read_vott_source_info(file_path, pym):
    # file ex:
    # Ubuntu:
    # file:/home/Drone_Source/Drone_001/Drone_001.mp4#t=305.533333,76a8e999e2d9232d8e26253551acb4b3-asset.json,time,tracking_time
    # Windows:
    # file:C:/Drone_Source/Drone_001/Drone_001.mp4#t=305.533333,76a8e999e2d9232d8e26253551acb4b3-asset.json,time,tracking_time

    if os.path.exists(file_path):
        pym.PY_LOG(False, 'D', py_name, 'vott_source_info.tmp: (path: %s) existed!' % file_path)
    else:
        pym.PY_LOG(False, 'E', py_name, 'vott_source_info.tmp: (path: %s) is not existed!' % file_path)
        return False, "", "", ""

    f = open(file_path, "r")
    # remove file:
    path = f.read()
    path = path[5:]
    vc = 0

    # get source video path
    vc = path.find('#')
    video_path = path[:vc]
    pym.PY_LOG(False, 'D', py_name, 'video_path: %s' % video_path)

    # get json file(this file will be created when user used auto track function)
    vc = path.find(',')
    file_name = path[vc+1:]
    pym.PY_LOG(False, 'D', py_name, 'file_name with time: %s' % file_name)

    # get tracking_time       
    tracking_time = 1         
    vc_tt = file_name.find(',')                                                                                                                             
    temp = file_name[vc_tt+1:]
    vc_tt = temp.find(',')   
    try:
        tracking_time = int(temp[vc_tt+1:])
        pym.PY_LOG(False, 'D', py_name, 'tracking_time: %d' % tracking_time)
    except:
        pym.PY_LOG(False, 'D', py_name, 'use default tracking_time 1')
        tracking_time = 1
                              
    vc = file_name.find(',')  
    json_file_name = file_name[:vc]
    pym.PY_LOG(False, 'D', py_name, 'json_file_name without time: %s' % json_file_name)
                              
    return True, video_path, json_file_name, tracking_time

def read_vott_target_path(file_path, json_file_name, pym):
    # this is a json file

    target_path = ''
    project_vott_file_path = ''
    json_file_path = ""

    if os.path.exists(file_path):
        pym.PY_LOG(False, 'D', py_name, 'vott_target_path.json: (path: %s) existed!' % file_path)
    else:
        pym.PY_LOG(False, 'E', py_name, 'vott_target_path.json: (path: %s) is not existed!' % file_path)
        return False, "", "", ""
    
    # open file
    f = open(file_path, 'r')
    content = json.loads(f.read())
    f.close()

    # read project.vott path from file
    target_path = content["options"]["folderPath"] + '/'
    pym.PY_LOG(False, 'D', py_name, 'get target path: %s' % target_path)

    project_vott_name = content["project_name"] + '.vott'
    pym.PY_LOG(False, 'D', py_name, 'get project.vott name : %s' % project_vott_name)

    project_vott_file_path = target_path + project_vott_name
    pym.PY_LOG(False, 'D', py_name, 'project_vott_file_path: %s' % project_vott_file_path)

    json_file_path = target_path + json_file_name
    pym.PY_LOG(False, 'D', py_name, 'get json file path: %s' % json_file_path)

    return True, target_path, project_vott_file_path , json_file_path


def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def show_error_msg_on_toast(title, msg):
    messagebox.showerror(title, msg)

def show_info_msg_on_toast(title, msg):
    messagebox.showinfo(title, msg)


def do_shutdown_log_and_show_error_msg(paras):
    '''
    paras:
        index 0: msg
        index 1: pym
        index 2: remove below tmp file switch
        index 3: vott_source_info
        index 4: vott_target_path
    '''
    msg = paras[0]
    pym = paras[1]
    pym.PY_LOG(True, 'E', py_name, '__process_terminate__' + msg + "\n\n\n\n")
    show_error_msg_on_toast("vott_tracker",msg + "\n" + "the details please refer log.txt(VoTT_NTUT/your OS/log/log.txt)!!")

    # if remove_switch = false that is for analyzing those data while error happened
    remove_switch = paras[2]
    if remove_switch:
        vott_source_info = paras[3]
        vott_target_path = paras[4]
        remove_file(vott_source_info)
        remove_file(vott_target_path)
    sys.exit()

def do_shutdown_log_with_all(pym, rvij, ppv, wvij, cvtr, paras):
#def do_shutdown_log_with_all(pym, rvij, wvij, cvtr, paras):
    '''
    paras:
        index 0: msg
        index 1: track_success
        index 2: vott_source_info
        index 3: vott_project_path
    '''

    msg = paras[0]
    track_success = paras[1]
    vott_source_info = paras[2]
    vott_target_path = paras[3]


    pym.PY_LOG(True, 'D', py_name, msg)
    rvij.shut_down_log('__done__')
    ppv.shut_down_log('__done__')
    wvij.shut_down_log('__done__')
    cvtr.shut_down_log('__done__\n\n\n\n')

    remove_file(vott_source_info)
    remove_file(vott_target_path)
    if track_success:
        show_info_msg_on_toast("vott tracker", "tracking objects successfully!!")
    else:
        show_info_msg_on_toast("vott tracker", "tracking objects failed!!")
    sys.exit()
