from Levels import commonfunctions as CFS

## checkpoint events for DeadReckon
starting_health = 105
bgm = CFS.sound_loader('./sounds/music/all.wav')

msg0 = CFS.create_messages(('Ghosts cross walls and close from behind.',))
def func0(gameObj, levelObj=None):
    levelObj.player.knife_equiped = False
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 9

msg1 = CFS.create_messages(('The patrol routes are only in the central halls.',))
def func1(gameObj, levelObj=None):
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 9

msg2 = CFS.create_messages(('Remember the outer passage; it is the safest way back.',))
def func2(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 9

msg3 = CFS.create_messages(('Route updated. Take the next opening.',))
def func3(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg3), gameObj.fps * 9

msg4 = CFS.create_messages(('Another sector cleared. Keep your pace.',))
def func4(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg4), gameObj.fps * 9

msg5 = CFS.create_messages(('The final stretch is ahead. Stay alert.',))
def func5(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg5), gameObj.fps * 9
