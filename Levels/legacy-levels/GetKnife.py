from Levels import commonfunctions as CFS

bgm = CFS.sound_loader('./sounds/music/bassanddrum.wav')

msg0 = CFS.create_messages((
    'The tunnel is held by fifteen fixed patrols.',
    'Wait for a gap before crossing the long corridors.',
))
def func0(gameObj, levelObj=None):
    levelObj.player.knife_equiped = False
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 10

msg1 = CFS.create_messages((
    'Knife acquired. Right-click to slash; you must be close to hit.',
    'A guard needs several hits, so attack between patrol passes.',
))
def func1(gameObj, levelObj=None):
    levelObj.player.knife_equiped = True
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 10

msg2 = CFS.create_messages((
    'The next patrol holds a narrow corridor. Flank if the timing is poor.',
))
def func2(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 8

msg3 = CFS.create_messages((
    'Final marker. Leave room to retreat after the last crossing.',
))
def func3(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg3), gameObj.fps * 8
