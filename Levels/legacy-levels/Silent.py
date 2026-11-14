from Levels import commonfunctions as CFS

## checkpoint events for Silent
starting_health = 80
bgm = CFS.sound_loader('./sounds/music/bassanddrum.wav')

msg0 = CFS.create_messages(('Ten patrols can hurt you, but none will chase.',))
def func0(gameObj, levelObj=None):
    levelObj.player.knife_equiped = False
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 9

msg1 = CFS.create_messages(('Learn their loops and cross one lane at a time.',))
def func1(gameObj, levelObj=None):
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 9

msg2 = CFS.create_messages(('The outer route is longer and leaves more room to recover.',))
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
