import pygame
from Levels import commonfunctions as CFS

## authored mission script for L14_RedCorridor

bgm = CFS.sound_loader('./sounds/music/bass1.wav')

msg0 = CFS.create_messages(
    ('A narrow corridor splits the room.',)
)
def func0(gameObj, levelObj=None):
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 6


msg1 = CFS.create_messages(
    ('Use the two openings to avoid the patrols.',)
)
def func1(gameObj, levelObj=None):
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 6


msg2 = CFS.create_messages(
    ('The extraction marker is on the far side.',)
)
def func2(gameObj, levelObj=None):
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 6

