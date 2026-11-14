from Levels import commonfunctions as CFS

## checkpoint events for C05_DeadAngle
starting_health = 120
bgm = CFS.sound_loader('./sounds/music/bass.wav')

msg0 = CFS.create_messages(('A patrol is hidden behind the first blind corner.',))
def func0(gameObj, levelObj=None):
    levelObj.player.knife_equiped = False
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 9

msg1 = CFS.create_messages(('The ghost ignores the wall. Break contact around the outside.',))
def func1(gameObj, levelObj=None):
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 9

msg2 = CFS.create_messages(('Re-enter through the lower gap when the lane clears.',))
def func2(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 9
