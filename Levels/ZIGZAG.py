import pygame
from Levels import commonfunctions as CFS

## script for mission ZIGZAG

bgm = CFS.sound_loader('./sounds/music/bass.wav')

## code for event 0 ::  
msg0 = CFS.create_messages(
            (
                'There is a mayhem out there!!',
                'Watch your steps and carefully move towards the right'
            )
        )
def func0(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    levelObj.player.knife_equiped = False
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 10



## code for event 1 ::  
msg1 = CFS.create_messages(
            (
                'Event 1 just got triggered',
                'This is automatic generation of message'
            )
        )
def func1(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    levelObj.player.knife_equiped = True
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 10

