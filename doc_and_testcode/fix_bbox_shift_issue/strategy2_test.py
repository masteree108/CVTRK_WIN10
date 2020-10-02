source = 29
fps = 15

interval = float(source / fps)
print("interval: %.2f" % interval)

interval_ct = interval
frame_ct = 0
for i in range(source):
    if i >= interval_ct and i <= interval_ct+1:
        frame_ct +=1
        interval_ct = interval_ct + interval
        print('interval_ct: %.2f' % interval_ct)
        
        if frame_ct < 15:
            print('save to json file, pick up frame number: %d' % i)
 
