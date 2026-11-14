from Levels import commonfunctions as CFS

## checkpoint events for C17_LastWindow
starting_health = 80
bgm = CFS.sound_loader('./sounds/music/all.wav')

msg0 = CFS.create_messages(('The extraction route crosses six sectors before doubling back.',))
def func0(gameObj, levelObj=None):
    levelObj.player.knife_equiped = True
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 9

msg1 = CFS.create_messages(('Patrols hold the doors. Ghosts cut across the barriers.',))
def func1(gameObj, levelObj=None):
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 9

msg2 = CFS.create_messages(('Collect the first charge before the center crossing.',))
def func2(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 9

msg3 = CFS.create_messages(('Use the lower pocket while the upper patrol turns.',))
def func3(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg3), gameObj.fps * 9

msg4 = CFS.create_messages(('The far cache is exposed; save a blast for the return chase.',))
def func4(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg4), gameObj.fps * 9

msg5 = CFS.create_messages(('The route folds back through the busiest court.',))
def func5(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg5), gameObj.fps * 9

msg6 = CFS.create_messages(('One last window. Wait for the patrol gap, then commit.',))
def func6(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg6), gameObj.fps * 9
