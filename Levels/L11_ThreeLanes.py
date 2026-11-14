import pygame
from Levels import commonfunctions as CFS

## authored mission script for L11_ThreeLanes

bgm = CFS.sound_loader('./sounds/music/bassanddrum.wav')

msg0 = CFS.create_messages(
    ('Three lanes lead across the yard.',)
)
def func0(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 6


msg1 = CFS.create_messages(
    ('The center is fastest; the sides are safer.',)
)
def func1(gameObj, levelObj=None):
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 6


msg2 = CFS.create_messages(
    ('Choose a route and reach the far marker.',)
)
def func2(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 6

