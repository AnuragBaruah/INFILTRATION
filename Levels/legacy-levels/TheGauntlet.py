from Levels import commonfunctions as CFS

## checkpoint events for TheGauntlet
starting_health = 75
bgm = CFS.sound_loader('./sounds/music/bass.wav')

msg0 = CFS.create_messages(('There is no straight safe line. Read the first patrol.',))
def func0(gameObj, levelObj=None):
    levelObj.player.knife_equiped = False
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 9

msg1 = CFS.create_messages(('Cross after its turn; the window is short.',))
def func1(gameObj, levelObj=None):
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 9

msg2 = CFS.create_messages(('Choose an exit before entering the central court.',))
def func2(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 9

msg3 = CFS.create_messages(("A ghost follows from behind; don't retreat into a cleared lane.",))
def func3(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg3), gameObj.fps * 9

msg4 = CFS.create_messages(('The longer east route gives space to reset.',))
def func4(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg4), gameObj.fps * 9

msg5 = CFS.create_messages(('The next patrol overlaps the doorway.',))
def func5(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg5), gameObj.fps * 9

msg6 = CFS.create_messages(('Save health for the narrow final gate.',))
def func6(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg6), gameObj.fps * 9
