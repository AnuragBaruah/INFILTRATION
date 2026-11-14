from Levels import commonfunctions as CFS

bgm = CFS.sound_loader('./sounds/music/bass.wav')

msg0 = CFS.create_messages((
    'Thirty-two patrols cover the long zigzag route.',
    'Use the alternating openings; the guards do not chase through walls.',
))
def func0(gameObj, levelObj=None):
    levelObj.player.knife_equiped = False
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 10

msg1 = CFS.create_messages((
    'The far marker is past the last patrol lane.',
    'Cross after the guard turns, then keep moving to extraction.',
))
def func1(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 10
