import csv, math



def extract_walls():
    with open('Default Dataset.csv') as f:
        r = list(csv.reader(f))

    walls = []
    t = 10
    print(len(r))
    for i in range(0, len(r), 2):
        p1 = r[i]
        p2 = r[i+1]
        p1 = [int(float(p1[0])), int(float(p1[1]))]
        p2 = [int(float(p2[0])), int(float(p2[1]))]
        if math.fabs(p1[0] - p2[0]) > math.fabs(p1[1] - p2[1]):
            p1[1] = p1[1] - t//2
            p2[1] = p2[1] + t//2
        else:
            p1[0] = p1[0] - t//2
            p2[0] = p2[0] + t//2
        grid1 = p1[0] // 1280, p1[1] // 720
        grid2 = p2[0] // 1280, p2[0] // 720
        n = 2
        if grid1 == grid2: n = 1
        grids = [grid1, grid2]
        for k in range(n):
            walls.append({'top_left' : tuple(p1), 'bottom_right' : tuple(p2), 'grid_coords' : grids[k]})
    return walls



