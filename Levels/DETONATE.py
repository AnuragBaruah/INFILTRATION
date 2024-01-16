import pygame
from Levels import commonfunctions as CFS

## script for mission DETONATE

bgm = CFS.sound_loader('./sounds/music/bassanddrum.wav')

## code for event 0 ::  
msg0 = CFS.create_messages(
            (
                'THE GHOSTS',
                'These can detect you if close enough, and chase you',
                'They can pass through walls',
                ' ',
                'Pick up those RC bombs', 
                'the number of bombs would be shown in the top right',
                'Press LeftMouseButton to plant a bomb', 
                'Press Spacebar to detonate the planted bombs',
                'Dont forget to move out of the way before detonating'
            )
        )
def func0(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 20



## code for event 1 ::  
msg1 = CFS.create_messages(
            (
                'A Lot of Enemies are there',
            )
        )
def func1(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 5



## code for event 2 ::  
msg2 = CFS.create_messages(
            (
                'Event 2 just got triggered',
                'This is automatic generation of message'
            )
        )
def func2(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 10

