from Levels import commonfunctions as CFS

## checkpoint events for PaperTrail
starting_health = 95
bgm = CFS.sound_loader('./sounds/music/bass1.wav')

msg0 = CFS.create_messages(('The route forms a figure eight; the first turn matters.',))
def func0(gameObj, levelObj=None):
    levelObj.player.knife_equiped = False
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 9

msg1 = CFS.create_messages(('The lower doorway reconnects behind the sorting wall.',))
def func1(gameObj, levelObj=None):
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 9

msg2 = CFS.create_messages(('The nearest gate is a dead end.',))
def func2(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 9

msg3 = CFS.create_messages(('Use the long hall while the patrol is north.',))
def func3(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg3), gameObj.fps * 9

msg4 = CFS.create_messages(('The return leg enters the room from the opposite side.',))
def func4(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg4), gameObj.fps * 9

msg5 = CFS.create_messages(('The ghost is close. Keep moving past the marker.',))
def func5(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg5), gameObj.fps * 9

msg6 = CFS.create_messages(('Final turn: return through the dispatch bay.',))
def func6(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg6), gameObj.fps * 9
