from Levels import commonfunctions as CFS

bgm = CFS.sound_loader('./sounds/music/bassanddrum.wav')

msg0 = CFS.create_messages((
    'The ghost pack can pass through walls and will close in quickly.',
    'Walk over a charge, left-click to plant, then press Space to detonate.',
    'Get clear before the blast. The three caches are your limited resources.',
))
def func0(gameObj, levelObj=None):
    levelObj.player.knife_equiped = False
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 16

msg1 = CFS.create_messages((
    'Forty-two ghosts and eighteen patrols remain across the next sectors.',
    'Use the outer route to split the chase before planting another charge.',
))
def func1(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 10

msg2 = CFS.create_messages((
    'The extraction marker is beyond the last crossing. Keep moving.',
))
def func2(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 8
