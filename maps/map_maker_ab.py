###___MAP___

import pickle
t = 50
#{'top_left' : (),  'bottom_right' : (), 'grid_coords' : ()},
walls = [
                {'top_left' : (0,0), 'bottom_right' : (1280, t), 'grid_coords' : (0,0)},
                {'top_left' : (0,0),  'bottom_right' : (t, 720), 'grid_coords' : (0,0)},
                {'top_left' : (0, 360),  'bottom_right' : (640, 360 + t), 'grid_coords' : (0,0)},
                {'top_left' : (1280, 0),  'bottom_right' : (1280 + t, 400), 'grid_coords' : (0,0)},
                {'top_left' : (1280, 0),  'bottom_right' : (1280 + t, 400), 'grid_coords' : (1, 0)},
                {'top_left' : (1280, 0),  'bottom_right' : (2560, t), 'grid_coords' : (1,0)},
                {'top_left' : (2560, 0),  'bottom_right' : (3840, t), 'grid_coords' : (2, 0)},
                {'top_left' : (3840, 0),  'bottom_right' : (5120, t), 'grid_coords' : (3, 0)},
                {'top_left' : (5120 - t, 0),  'bottom_right' : (5120, 720), 'grid_coords' : (3,0)},

                {'top_left' : (3740, 360),  'bottom_right' : (3740 + t, 640), 'grid_coords' : (2,0)},
                {'top_left' : (2460, 360),  'bottom_right' : (2460 + t, 640), 'grid_coords' : (1,0)},
                
                {'top_left' : (0, 720),  'bottom_right' : (768, 720 + t), 'grid_coords' : (0,0)},
                {'top_left' : (0, 720),  'bottom_right' : (768, 720 + t), 'grid_coords' : (0,1)},
                {'top_left' : (1088, 720),  'bottom_right' : (1280, 720 + t), 'grid_coords' : (0,0)},
                {'top_left' : (1088, 720),  'bottom_right' : (1280, 720 + t), 'grid_coords' : (0,1)},
                {'top_left' : (1280, 720),  'bottom_right' : (2560, 720 + t), 'grid_coords' : (1,1)},
                {'top_left' : (1280, 720),  'bottom_right' : (2560, 720 + t), 'grid_coords' : (1,0)},
                {'top_left' : (2560, 720),  'bottom_right' : (3840, 720 + t), 'grid_coords' : (2,1)},
                {'top_left' : (2560, 720),  'bottom_right' : (3840, 720 + t), 'grid_coords' : (2,0)},
                {'top_left' : (3840, 720),  'bottom_right' : (4160, 720 + t), 'grid_coords' : (3,0)},
                {'top_left' : (3840, 720),  'bottom_right' : (4160, 720 + t), 'grid_coords' : (3,1)},
                {'top_left' : (4480, 720),  'bottom_right' : (5120, 720 + t), 'grid_coords' : (3,0)},
                {'top_left' : (4480, 720),  'bottom_right' : (5120, 720 + t), 'grid_coords' : (3,1)},
                {'top_left' : (0, 720),  'bottom_right' : (t, 1440), 'grid_coords' : (0,1)},
                {'top_left' : (1280, 720),  'bottom_right' : (1280 + t, 1440), 'grid_coords' : (0,1)},
                {'top_left' : (1280, 720),  'bottom_right' : (1280 + t, 1440), 'grid_coords' : (1,1)},
                {'top_left' : (1600, 912),  'bottom_right' : (1920, 1232), 'grid_coords' : (1,1)},
                {'top_left' : (2560, 720),  'bottom_right' : (2560 + t, 1232), 'grid_coords' : (1,1)},
                {'top_left' : (2560, 720),  'bottom_right' : (2560 + t, 1232), 'grid_coords' : (2,1)},
                {'top_left' : (2560, 1232),  'bottom_right' : (3520, 1232 + t), 'grid_coords' : (2,1)},
                {'top_left' : (5120 - t, 720),  'bottom_right' : (5120, 1440), 'grid_coords' : (3,1)},
                {'top_left' : (320, 1440),  'bottom_right' : (1280, 1440 + t), 'grid_coords' : (0,1)},
                {'top_left' : (320, 1440),  'bottom_right' : (1280, 1440 + t), 'grid_coords' : (0,2)},
                {'top_left' : (1280, 1440),  'bottom_right' : (2560, 1440 + t), 'grid_coords' : (1,1)},
                {'top_left' : (1280, 1440),  'bottom_right' : (2560, 1440 + t), 'grid_coords' : (1,2)},
                {'top_left' : (3520, 1440),  'bottom_right' : (3840, 1440 + t), 'grid_coords' : (2,1)},
                {'top_left' : (3520, 1440),  'bottom_right' : (3840, 1440 + t), 'grid_coords' : (2,2)},
                {'top_left' : (3840, 1440),  'bottom_right' : (4160, 1440 + t), 'grid_coords' : (3,1)},
                {'top_left' : (3840, 1440),  'bottom_right' : (4160, 1440 + t), 'grid_coords' : (3,2)},
                {'top_left' : (4480, 1440),  'bottom_right' : (5120, 1440 + t), 'grid_coords' : (3,1)},
                {'top_left' : (4480, 1440),  'bottom_right' : (5120, 1440 + t), 'grid_coords' : (3,2)},
                {'top_left' : (5120 - t, 1440),  'bottom_right' : (5120, 2160), 'grid_coords' : (3,2)},
                {'top_left' : (4320, 1760),  'bottom_right' : (4320 + t, 2160), 'grid_coords' : (3,2)},
                {'top_left' : (4320, 2160),  'bottom_right' : (4320 + t, 2320), 'grid_coords' : (3,3)},
                {'top_left' : (5120 - t, 2160),  'bottom_right' : (5120, 2880), 'grid_coords' : (3,3)},
                {'top_left' : (4032, 2480),  'bottom_right' : (4800, 2672), 'grid_coords' : (3,3)},
                {'top_left' : (3840, 2880 - t),  'bottom_right' : (5120, 2880), 'grid_coords' : (3,3)},
                {'top_left' : (2560, 2880 - t),  'bottom_right' : (3840, 2880), 'grid_coords' : (2,3)},
                {'top_left' : (1280, 2880 - t),  'bottom_right' : (2560, 2880), 'grid_coords' : (1,3)},
                {'top_left' : (0, 2880 - t),  'bottom_right' : (1280, 2880), 'grid_coords' : (0,3)},
                {'top_left' : (0, 2160),  'bottom_right' : (t, 2880), 'grid_coords' : (0,3)},
                {'top_left' : (0, 1440),  'bottom_right' : (t, 2160), 'grid_coords' : (0,2)},
                {'top_left' : (0, 2160),  'bottom_right' : (1280, 2160 + t), 'grid_coords' : (0,2)},
                {'top_left' : (0, 2160),  'bottom_right' : (1280, 2160 + t), 'grid_coords' : (0,3)},
                {'top_left' : (1280, 2160),  'bottom_right' : (2560, 2160 + t), 'grid_coords' : (1,2)},
                {'top_left' : (1280, 2160),  'bottom_right' : (2560, 2160 + t), 'grid_coords' : (1,3)},
                {'top_left' : (2560, 2160),  'bottom_right' : (2880, 2160 + t), 'grid_coords' : (2,2)},
                {'top_left' : (2560, 2160),  'bottom_right' : (2880, 2160 + t), 'grid_coords' : (2,3)},
                {'top_left' : (3200, 2160),  'bottom_right' : (3520, 2160 + t), 'grid_coords' : (2,2)},
                {'top_left' : (3200, 2160),  'bottom_right' : (3520, 2160 + t), 'grid_coords' : (2,3)},
                {'top_left' : (3520, 2160),  'bottom_right' : (3520 + t, 2880), 'grid_coords' : (2,3)},
                {'top_left' : (320, 2160),  'bottom_right' : (320 + t, 2480), 'grid_coords' : (0,3)},
                {'top_left' : (960, 2160),  'bottom_right' : (960 + t, 2480), 'grid_coords' : (0,3)},
                {'top_left' : (1920, 2160),  'bottom_right' : (1920 + t, 2480), 'grid_coords' : (1,3)},
                {'top_left' : (640, 2480),  'bottom_right' : (640 + t, 2880), 'grid_coords' : (0,3)},
                {'top_left' : (1600, 2480),  'bottom_right' : (1600 + t, 2880), 'grid_coords' : (1,3)},
                {'top_left' : (2240, 2480),  'bottom_right' : (2240 + t, 2880), 'grid_coords' : (1,3)},
                {'top_left' : (0, 1760),  'bottom_right' : (1280, 1760 + t), 'grid_coords' : (0,2)},
                {'top_left' : (1280, 1760),  'bottom_right' : (1920, 1760 + t), 'grid_coords' : (1,2)},
                {'top_left' : (2240, 1760),  'bottom_right' : (2560, 1760 + t), 'grid_coords' : (1,2)},
                {'top_left' : (2560, 1760),  'bottom_right' : (3520, 1760 + t), 'grid_coords' : (2,2)},
                {'top_left' : (3520, 1440),  'bottom_right' : (3520 + t, 2160), 'grid_coords' : (2,2)}
                
            ]
things = [
                 {},
                 {}
            ]

data = {'walls' : walls}
import make_the_map
walls = make_the_map.extract_walls()
data = {'walls' : walls}
with open('Level0/L0.map', 'wb') as f:
    pickle.dump(data, f)
