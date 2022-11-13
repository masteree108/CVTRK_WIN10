# 1.build vott_tracker.exe
# note 1: if your os is windows10 please execute below command on the anaconda terminal
# note 2: this buiild_exe.sh that needs to setup module please as follows
# pip install pyinstaller

pyinstaller -F --noconsole --onefile ./vott_tracker.py

# 2. copy vott_tracker.exe to the project address
# please execute below command on the WSL terminal, it can hide above command like below
#pyinstaller -F --noconsole --onefile ./vott_tracker.py
# and execute ./build_exe.sh
cp -f ./dist/vott_tracker.exe ../VoTT_NTUT_WIN10/NTUT/exe/vott_tracker.exe
cp -f ./dist/vott_tracker.exe ./vott_tracker.exe
cp -af ./NTUT/yolo-coco_v3 ../VoTT_NTUT_WIN10/NTUT/
rm -rf dist
rm -rf __pycache__
rm -rf build
rm *.spec
