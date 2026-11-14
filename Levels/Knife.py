from Levels import commonfunctions as CFS

## checkpoint events for Knife
starting_health = 130
bgm = CFS.sound_loader('./sounds/music/bassanddrum.wav')

msg0 = CFS.create_messages(('MOVE: KB/MOUSE W/S + cursor | CONTROLLER left stick.', 'SLASH: KB/MOUSE right mouse | CONTROLLER RB.'))
def func0(gameObj, levelObj=None):
    levelObj.player.knife_equiped = True
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 9

msg1 = CFS.create_messages(('They were expecting someone else.',))
def func1(gameObj, levelObj=None):
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 9

msg2 = CFS.create_messages(('Nobody gets out of this one clean.',))
def func2(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 9
