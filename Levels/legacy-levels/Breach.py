from Levels import commonfunctions as CFS

## checkpoint events for Breach
starting_health = 100
bgm = CFS.sound_loader('./sounds/music/bass1.wav')

msg0 = CFS.create_messages(('Weak patrols hold the breach; ghosts close in from behind walls.',))
def func0(gameObj, levelObj=None):
    levelObj.player.knife_equiped = True
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 9

msg1 = CFS.create_messages(('Use the knife only when a patrol blocks the doorway.',))
def func1(gameObj, levelObj=None):
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 9

msg2 = CFS.create_messages(('Save bombs for the crowded room beyond the breach.',))
def func2(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 9

msg3 = CFS.create_messages(('Route updated. Take the next opening.',))
def func3(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg3), gameObj.fps * 9
