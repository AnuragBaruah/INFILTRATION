"""Build the 46-mission campaign that follows the four focused tutorials.

Run from the repository root: ``python maps/organic_campaign.py``.
The four tutorial packages are retained; this generator replaces the playable
campaign registry and generates every main-campaign map and mission script.
"""
from __future__ import annotations

import pygame
import ai_agent_map_maker as world

W, H = world.CELL_W, world.CELL_H

# id, title, layout motif, (columns, rows), checkpoint count.
# The campaign alternates spatial problems and pressure while making
# trap-and-blast play its central loop. Enemy count rises only as bombs and
# encounter structure also give the player more tools and choice.
DESIGNS = [
 ("SaltwindCauseway", "Saltwind Causeway", "yard", (1,1), 3),
 ("TwinSwitches", "Twin Switches", "braid", (2,1), 4),
 ("SluiceGate", "Sluice Gate", "sluice", (1,2), 4),
 ("AshCourt", "Ash Court", "pockets", (1,1), 3),
 ("UnderpassRelay", "Underpass Relay", "underpass", (2,1), 4),
 ("FloodplainLoop", "Floodplain Loop", "loop", (2,2), 5),
 ("BlindTurn", "Blind Turn", "dogleg", (2,1), 4),
 ("PaperDistrict", "Paper District", "figure8", (2,2), 5),
 ("NightDocks", "Night Docks", "islands", (2,2), 5),
 ("NarrowGauge", "Narrow Gauge", "corridor", (2,1), 4),
 ("SplitSignal", "Split Signal", "switchback", (2,1), 4),
 ("ParcelRun", "Parcel Run", "parcel", (2,2), 5),
 ("FortBracket", "Fort Bracket", "courts", (2,2), 5),
 ("FreightReturn", "Freight Return", "meander", (3,1), 5),
 ("PierBlackout", "Pier Blackout", "blackout", (2,2), 5),
 ("ColdStore", "Cold Store", "spiral", (2,2), 5),
 ("WatchhouseGauntlet", "Watchhouse Gauntlet", "gauntlet", (3,1), 6),
 ("NarrowWorks", "Narrow Works", "dogleg", (2,1), 4),
 ("GlassYard", "Glass Yard", "islands", (2,2), 5),
 ("LongNight", "Long Night", "spiral", (3,2), 6),
 ("LastTrain", "Last Train", "final", (3,2), 6),
 ("SawtoothMile", "Sawtooth Mile", "switchback", (2,1), 4),
 ("PumpStation", "Pump Station", "sluice", (2,2), 5),
 ("FreightBraid", "Freight Braid", "braid", (2,2), 5),
 ("ThreeCourtyards", "Three Courtyards", "courts", (3,1), 5),
 ("FalseShortcut", "False Shortcut", "underpass", (2,2), 5),
 ("DispatchLoop", "Dispatch Loop", "figure8", (2,2), 6),
 ("CargoMaze", "Cargo Maze", "parcel", (3,2), 6),
 ("SplitBasin", "Split Basin", "loop", (2,2), 5),
 ("BlindRelay", "Blind Relay", "dogleg", (3,1), 5),
 ("FoundrySpiral", "Foundry Spiral", "spiral", (2,2), 6),
 ("NorthCrossing", "North Crossing", "crossing", (2,2), 5),
 ("BrokenYard", "Broken Yard", "pockets", (2,2), 5),
 ("LongReturn", "Long Return", "meander", (3,1), 6),
 ("TwoCharges", "Two Charges", "switchback", (2,2), 5),
 ("BreachYard", "Breach Yard", "final", (2,1), 4),
 ("Redoubt", "Redoubt", "courts", (2,2), 5),
 ("Crosswind", "Crosswind", "braid", (2,2), 5),
 ("SilentPier", "Silent Pier", "blackout", (3,1), 5),
 ("DeadAngle", "Dead Angle", "figure8", (2,2), 5),
 ("PressureValve", "Pressure Valve", "sluice", (2,2), 5),
 ("GhostLine", "Ghost Line", "underpass", (3,1), 5),
 ("NoSafeCenter", "No Safe Center", "islands", (2,2), 5),
 ("FinalWindow", "Final Window", "gauntlet", (3,1), 6),
 ("LastPlatform", "Last Platform", "final", (3,2), 6),
 ("ExtractionRoute", "Extraction Route", "meander", (3,2), 6),
]

# Campaign encounter identity: pickups, basic chasers, weak patrols, health,
# knife access, and encounter waves. Several missions intentionally ask the
# player to ration bombs or mix a bomb trap with a small knife duel.
MISSION_TUNING = {
 "SaltwindCauseway": (2,2,0,110,False,1),
 "TwinSwitches": (2,4,0,105,False,2),
 "SluiceGate": (3,3,1,105,False,2),
 "AshCourt": (2,3,1,100,False,2),
 "UnderpassRelay": (1,4,1,100,False,3),
 "FloodplainLoop": (3,4,1,100,False,3),
 "BlindTurn": (2,3,1,95,False,2),
 "PaperDistrict": (2,5,0,100,False,3),
 "NightDocks": (3,4,1,95,False,3),
 "NarrowGauge": (1,2,1,110,True,2),
 "SplitSignal": (2,4,0,100,False,2),
 "ParcelRun": (1,4,1,95,False,3),
 "FortBracket": (2,3,2,95,True,2),
 "FreightReturn": (2,5,0,95,False,3),
 "PierBlackout": (1,5,2,90,False,3),
 "ColdStore": (3,4,1,100,False,2),
 "WatchhouseGauntlet": (2,5,1,90,False,3),
 "NarrowWorks": (1,5,1,90,False,3),
 "GlassYard": (3,5,2,90,False,3),
 "LongNight": (2,6,1,85,False,3),
 "LastTrain": (3,4,2,90,False,3),
 "SawtoothMile": (1,3,2,100,True,2),
 "PumpStation": (2,5,0,90,False,3),
 "FreightBraid": (3,4,2,90,False,2),
 "ThreeCourtyards": (1,2,2,100,True,2),
 "FalseShortcut": (1,5,2,85,False,3),
 "DispatchLoop": (2,4,1,90,False,3),
 "CargoMaze": (3,6,0,85,False,3),
 "SplitBasin": (2,5,1,85,False,3),
 "BlindRelay": (1,6,1,85,False,3),
 "FoundrySpiral": (2,5,2,80,False,3),
 "NorthCrossing": (3,5,3,90,True,2),
 "BrokenYard": (2,6,1,80,False,3),
 "LongReturn": (1,6,2,80,False,3),
 "TwoCharges": (2,5,1,85,False,3),
 "BreachYard": (2,4,2,85,True,3),
 "Redoubt": (1,3,2,80,True,3),
 "Crosswind": (2,6,3,80,False,3),
 "SilentPier": (3,5,2,80,False,3),
 "DeadAngle": (1,6,1,80,False,3),
 "PressureValve": (2,6,2,75,False,3),
 "GhostLine": (3,5,1,75,False,3),
 "NoSafeCenter": (1,6,2,75,False,3),
 "FinalWindow": (2,7,2,75,False,3),
 "LastPlatform": (3,4,2,75,True,3),
 "ExtractionRoute": (2,7,3,70,False,3),
}


def wall(x, y, w, h):
    return world.wall_rect(x, y, w, h)


def segmented_v(x, gap, *, y=25, height=670, width=38, opening=250):
    lo, hi = gap-opening//2, gap+opening//2
    return [wall(x,y,width,max(0,lo-y)), wall(x,hi,width,max(0,y+height-hi))]


def segmented_h(y, gap, *, x=25, length=1230, width=38, opening=250):
    lo, hi = gap-opening//2, gap+opening//2
    return [wall(x,y,max(0,lo-x),width), wall(hi,y,max(0,x+length-hi),width)]


def layout(spec):
    _name,_title,(cols,rows),kind,*_rest = spec
    walls=[]
    for cx in range(1,cols):
        for cy in range(rows):
            walls += segmented_v(cx*W-20,cy*H+(205 if (cx+cy)%2 else 505),y=cy*H+15,height=H-30,width=40,opening=285)
    for cy in range(1,rows):
        for cx in range(cols):
            walls += segmented_h(cy*H-20,cx*W+(920 if (cx+cy)%2 else 350),x=cx*W+15,length=W-30,width=40,opening=300)
    for col in range(cols):
      for row in range(rows):
        x,y=col*W,row*H
        motif={
          "yard":[(350,100,38,220),(390,100,210,38),(760,390,250,38),(760,428,38,170)],
          "braid":[(230,100,260,38),(490,138,38,220),(650,455,300,38),(950,260,38,230)],
          "sluice":[(190,140,38,300),(228,140,260,38),(600,330,38,270),(638,562,250,38)],
          "pockets":[(260,100,230,38),(490,138,38,190),(700,390,260,38),(960,220,38,210)],
          "underpass":[(210,100,38,210),(248,272,240,38),(580,430,38,210),(618,600,250,38)],
          "loop":[(200,100,250,38),(412,138,38,230),(710,400,270,38),(942,438,38,210)],
          "dogleg":[(250,80,38,250),(288,292,240,38),(700,420,38,230),(738,612,260,38)],
          "figure8":[(180,120,38,250),(218,332,260,38),(650,90,250,38),(862,128,38,230)],
          "islands":[(280,160,150,150),(730,410,180,130),(960,160,38,230),(510,500,180,38)],
          "corridor":[(230,90,38,210),(268,262,280,38),(690,430,38,220),(728,612,280,38)],
          "switchback":[(200,110,280,38),(442,148,38,240),(700,390,280,38),(942,200,38,230)],
          "parcel":[(200,120,38,250),(238,332,260,38),(660,90,38,260),(698,312,260,38)],
          "courts":[(220,120,220,38),(402,158,38,210),(700,420,260,38),(922,220,38,240)],
          "meander":[(240,100,38,240),(278,302,270,38),(680,390,38,250),(718,602,280,38)],
          "blackout":[(220,100,38,250),(258,312,250,38),(650,380,38,240),(688,580,260,38)],
          "spiral":[(180,100,300,38),(442,138,38,260),(600,500,320,38),(882,250,38,288)],
          "gauntlet":[(220,90,38,240),(258,292,260,38),(660,390,38,250),(698,602,260,38)],
          "final":[(200,80,38,250),(238,292,250,38),(620,380,38,250),(658,592,250,38),(990,120,38,250)],
          "crossing":[(370,110,250,42),(660,300,250,42),(370,500,250,42),(620,155,42,145),(910,340,42,160)],
        }[kind]
        for rx,ry,rw,rh in motif:
          if (col+row)%2: rx=W-rx-rw
          if (col+2*row)%3==1: ry=H-ry-rh
          walls.append(wall(x+rx,y+ry,rw,rh))
    return world.outer_walls(cols,rows)+walls


def rects_from(walls):
    return [pygame.Rect(w["top_left"],(w["bottom_right"][0]-w["top_left"][0],w["bottom_right"][1]-w["top_left"][1])) for w in walls]


RETURN_LEG_IDS={"PaperDistrict","FreightReturn","LastTrain","DispatchLoop","LongReturn","ExtractionRoute"}


def markers_for(size,count,level_id):
    cols,rows=size
    cells=[(cx,cy) for cy in range(rows) for cx in (range(cols) if cy%2==0 else range(cols-1,-1,-1))]
    cell_indices=[min(len(cells)-1, i*len(cells)//count) for i in range(count)]
    if level_id in RETURN_LEG_IDS and count>=4 and len(cells)>1:
        previous_sector=next((index for index in reversed(cell_indices[:-1]) if index!=cell_indices[-1]),None)
        if previous_sector is not None:
            cell_indices[-1]=previous_sector
    local=((220,535),(660,160),(1070,515),(900,350),(360,300),(650,560))
    points=[]
    for i in range(count):
        cell=cells[cell_indices[i]]
        dx,dy=local[i%len(local)]
        points.append((cell[0]*W+dx,cell[1]*H+dy))
    if len(set(points)) != len(points):
        raise ValueError(f"duplicate mission markers in {size} / {count}")
    return points


def validate(spec,data):
    """Check spawn, checkpoint and patrol-pair accessibility before packaging."""
    name,title,(cols,rows),kind,markers,weak,basic,health,knife,bombs,waves=spec
    width,height=cols*W,rows*H; step=20
    rects=rects_from([w for group in data["walls"].values() for w in group])
    nx,ny=width//step,height//step
    clear=bytearray(nx*ny)
    for gy in range(ny):
      for gx in range(nx):
        p=pygame.Rect(gx*step,gy*step,50,50)
        clear[gy*nx+gx]=not any(p.colliderect(r) for r in rects)
    sx,sy=data["player_data"]; start=(sy//step)*nx+sx//step
    if not clear[start]: raise ValueError(f"{name} spawn intersects a wall")
    seen={start}; todo=[start]
    while todo:
      i=todo.pop(); x,y=i%nx,i//nx
      for xx,yy in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        j=yy*nx+xx
        if 0<=xx<nx and 0<=yy<ny and clear[j] and j not in seen:
          seen.add(j); todo.append(j)
    def reachable_marker(p):
      mx,my=p
      for gy in range(max(0,my//step-3),min(ny,my//step+1)):
       for gx in range(max(0,mx//step-3),min(nx,mx//step+1)):
        i=gy*nx+gx
        if i in seen and gx*step<=mx<gx*step+50 and gy*step<=my<gy*step+50:return True
      return False
    for n,p in enumerate(data["mission_pointers"],1):
      if not reachable_marker(p):
        choices=[]
        for gy in range(ny):
          for gx in range(nx):
            i=gy*nx+gx
            if i in seen and clear[i]:
              q=(gx*step+25,gy*step+25)
              choices.append(((q[0]-p[0])**2+(q[1]-p[1])**2,q))
        distance,q=min(choices,key=lambda item:item[0])
        if distance**.5>220: raise ValueError(f"{name} checkpoint {n} is unreachable near {p}")
        data["mission_pointers"][n-1]=q
        print(f"  {name}: nudged checkpoint {n} from {p} to walkable point {q}")
    for n,p in enumerate(data["bomb_positions"],1):
      if not reachable_marker(p):
        choices=[]
        for gy in range(ny):
          for gx in range(nx):
            i=gy*nx+gx
            if i in seen and clear[i]:
              q=(gx*step+25,gy*step+25)
              choices.append(((q[0]-p[0])**2+(q[1]-p[1])**2,q))
        distance,q=min(choices,key=lambda item:item[0])
        if distance**.5>220: raise ValueError(f"{name} charge pickup {n} is unreachable near {p}")
        data["bomb_positions"][n-1]=q
        print(f"  {name}: nudged charge pickup {n} from {p} to walkable point {q}")
    for i in range(0,len(data["path_nodes"]),2):
      a,b=data["path_nodes"][i:i+2]
      if (pygame.Vector2(a).distance_to(b)<world.MIN_PATROL_NODE_DISTANCE
          or any(r.collidepoint(a) or r.collidepoint(b) or r.clipline(a,b) for r in rects)):
        raise ValueError(f"{name} patrol pair {i//2+1} is invalid")
    for x,y,_kind in data["enemy_data"]:
      if x<15 or y<15 or x+50>width-15 or y+50>height-15 or any(pygame.Rect(x,y,50,50).colliderect(r) for r in rects):
        raise ValueError(f"{name} enemy spawn intersects a wall or boundary: {(x,y)}")


def build(spec):
    name,title,size,kind,markers,weak_count,basic_count,health,knife,bomb_count,wave_count=spec
    walls=layout(spec); rects=rects_from(walls); enemies=[]; nodes=[]; lines=[]
    def open_actor(x,y):
      return (15<=x and 15<=y and x+50<=size[0]*W-15 and y+50<=size[1]*H-15
              and not any(pygame.Rect(x,y,50,50).colliderect(r) for r in rects))
    def away(x,y,margin=150):
      return all((x-ex)**2+(y-ey)**2>=margin**2 for ex,ey,_ in enemies)
    for i in range(weak_count):
      route_index=min(len(markers)-1,1+(i*(len(markers)-1)//max(1,weak_count)))
      wanted=markers[route_index]; found=None
      for radius in range(0,321,20):
        if found: break
        for dy in range(-radius,radius+1,20):
          for dx in range(-radius,radius+1,20):
            if max(abs(dx),abs(dy))!=radius: continue
            x,y=wanted[0]+dx-25,wanted[1]+dy-25
            for a,b in (((x-135,y+25),(x+165,y+25)),((x+25,y-135),(x+25,y+165))):
              if open_actor(x,y) and away(x,y,180) and not any(r.clipline(a,b) for r in rects):
                found=(x,y,a,b); break
            if found: break
          if found: break
      if not found: raise ValueError(f"{name}: cannot place patrol {i+1} near checkpoint {route_index+1}")
      x,y,a,b=found; enemies.append((x,y,"weak")); n=len(nodes); nodes += [a,b]; lines += [(n+1,),(n,)]
    # Chasers are deliberately placed in small packs near encounter markers.
    # They begin outside the bomb radius, detect the player, and can be lured
    # into a planted 300x300 blast instead of being scattered across the map.
    pack_count=min(wave_count,len(markers)-1,basic_count)
    pack_sizes=[basic_count//pack_count+(1 if i<basic_count%pack_count else 0) for i in range(pack_count)]
    for pack_index,pack_size in enumerate(pack_sizes):
      route_index=(1 if pack_count==1 else
                   1+round(pack_index*(len(markers)-2)/(pack_count-1)))
      route_index=min(route_index,len(markers)-1)
      mx,my=markers[route_index]
      spawned=[]
      for radius in (180,220,260,300):
        if len(spawned)>=pack_size: break
        for dy in range(-radius,radius+1,40):
          for dx in range(-radius,radius+1,40):
            if max(abs(dx),abs(dy))!=radius: continue
            x,y=mx+dx-25,my+dy-25
            if not open_actor(x,y) or (x-80)**2+(y-335)**2<=380**2: continue
            if any((x-ex)**2+(y-ey)**2<75**2 for ex,ey,_ in enemies): continue
            if any((x-ex)**2+(y-ey)**2<75**2 for ex,ey in spawned): continue
            spawned.append((x,y))
            if len(spawned)>=pack_size: break
          if len(spawned)>=pack_size: break
      if len(spawned)<pack_size:
        raise ValueError(f"{name}: cannot fit chaser pack {pack_index+1} near checkpoint {route_index+1}")
      enemies.extend((x,y,"basic") for x,y in spawned)

      # Every basic enemy needs a valid patrol graph before it can begin
      # chasing. Give each encounter pack a nearby, wall-clear patrol segment.
      patrol_pair=None
      node_pairs=(((160,0),(-160,0)),((0,160),(0,-160)),((150,150),(-150,-150)),((150,-150),(-150,150)))
      for radius in range(0,601,40):
        if patrol_pair: break
        for sy in range(-radius,radius+1,40):
          for sx in range(-radius,radius+1,40):
            if max(abs(sx),abs(sy))!=radius: continue
            center=(mx+sx,my+sy)
            for (adx,ady),(bdx,bdy) in node_pairs:
              a=(center[0]+adx,center[1]+ady); b=(center[0]+bdx,center[1]+bdy)
              if (all(15<=p[0]<size[0]*W-15 and 15<=p[1]<size[1]*H-15
                      and not any(r.collidepoint(p) for r in rects) for p in (a,b))
                      and not any(r.clipline(a,b) for r in rects)):
                patrol_pair=(a,b); break
            if patrol_pair: break
          if patrol_pair: break
      if patrol_pair is None:
        raise ValueError(f"{name}: cannot add a clear patrol segment for chaser pack {pack_index+1}")
      n=len(nodes); nodes.extend(patrol_pair); lines.extend(((n+1,),(n,)))
    bomb_positions=[]
    pickup_targets=[markers[min(len(markers)-1,i*len(markers)//bomb_count)] for i in range(bomb_count)]
    for target in pickup_targets:
      candidates=sorted(((x,y) for y in range(80,size[1]*H-40,80) for x in range(80,size[0]*W-40,80)),key=lambda p:(p[0]-target[0])**2+(p[1]-target[1])**2)
      pos=next((p for p in candidates
                if not any(pygame.Rect(p[0],p[1],50,50).colliderect(r) for r in rects)
                and p not in bomb_positions
                and all((p[0]-ex)**2+(p[1]-ey)**2>=130**2 for ex,ey,_ in enemies)
                and all((p[0]-bx)**2+(p[1]-by)**2>=160**2 for bx,by in bomb_positions)),None)
      if pos is None: raise ValueError(f"{name}: no walkable charge pickup")
      bomb_positions.append(pos)
    data={"walls":world.grid_wall_map(walls,*size),"path_nodes":nodes,"path_lines":lines,"mission_pointers":list(markers),"enemy_data":enemies,"player_data":(80,335),"bomb_positions":bomb_positions}
    validate(spec,data)
    return data


def messages_for(spec):
    name,title,_size,_kind,markers,*_rest=spec
    # One short, atmospheric opener per mission. Later checkpoints are silent.
    return [f"Dispatch: {title} was listed as clear. The report was wrong."]+[""]*(len(markers)-1)


def main():
    pygame.init(); pygame.display.set_mode((W,H))
    tutorial_ids=["Move","Patrol","Knife","Bombs"]
    registry=[("Move","Move"),("Patrol","Patrol"),("Knife","Knife"),("Bombs","Bombs")]
    for index,design in enumerate(DESIGNS):
      name,title,kind,size,count=design
      bombs,basic,weak,health,knife,waves=MISSION_TUNING[name]
      markers=markers_for(size,count,name)
      spec=(name,title,size,kind,markers,weak,basic,health,knife,bombs,waves)
      data=build(spec)
      playable={"name":name,"size":size,"health":health,"knife":knife,"checkpoint_count":len(markers),"messages":messages_for(spec)}
      world.write_level(playable, data, index+len(tutorial_ids), write_source=False)
      registry.append((name,title))
    ids=[level_id for level_id,_ in registry]
    (world.LEVELS/"Level-Names.txt").write_text("# Internal id | Mission title\n"+"\n".join(f"{i}|{title}" for i,title in registry)+"\n",encoding="utf-8")
    (world.LEVELS/"__init__.py").write_text("__all__ = "+repr(ids)+"\n",encoding="utf-8")
    pygame.quit()
    print(f"Generated a 50-level set: 4 tutorials and {len(DESIGNS)} campaign missions.")


if __name__=="__main__": main()
