import pygame
from Levels import commonfunctions as CFS

## authored mission script for L03_TheLongHall

bgm = CFS.sound_loader('./sounds/music/bassanddrum.wav')

msg0 = CFS.create_messages(
    ('The hall narrows ahead.',)
)
def func0(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 6


msg1 = CFS.create_messages(
    ('Take the side opening before the guard turns.',)
)
def func1(gameObj, levelObj=None):
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 6


msg2 = CFS.create_messages(
    ('Clear the final checkpoint.',)
)
def func2(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 6

