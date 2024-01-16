###___MAP___

import pickle
t = 20
with open('map.txt','r') as f:
    a=f.readlines()
    L=[]
    for i in a:
        l=i.rstrip('\n').split('.')
        print(l)
        d={}
        d['top_left']=[int(l[0]),int(l[1])]
        d['bottom_right']=[int(l[2]),int(l[3])]
        d['grid_coords']=tuple([int(l[4]),int(l[5])])
        d['orientation']=int(l[6])
        L.append(d)
for i in L:
    if i['orientation']==0:
        i['top_left'][0]=int((((i['top_left'][0])*1280)//30))
        i['top_left'][1]=int((((i['top_left'][1])*720)//17)-t)
        i['top_left']=tuple(i['top_left'])
        i['bottom_right'][0]=int((((i['bottom_right'][0])*1280)//30))
        i['bottom_right'][1]=int((((i['bottom_right'][1])*720)//17)+t)
        i['bottom_right']=tuple(i['bottom_right'])
        
    elif i['orientation']==1:
        i['top_left'][0]=int((((i['top_left'][0])*1280)//30)-t)
        i['top_left'][1]=int((((i['top_left'][1])*720)//17))
        i['top_left']=tuple(i['top_left'])
        i['bottom_right'][0]=int((((i['bottom_right'][0])*1280)//30)+t)
        i['bottom_right'][1]=int((((i['bottom_right'][1])*720)//17))
        i['bottom_right']=tuple(i['bottom_right'])
walls=L
print(walls)
            
data = {'walls' : walls}
with open('Level0/L0.map', 'wb') as f:
    pickle.dump(data, f)
