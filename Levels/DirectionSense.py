import pygame
from Levels import commonfunctions as CFS

## script for mission DirectionSense

bgm = CFS.sound_loader('./sounds/music/all.wav')

## code for event 0 ::  
msg0 = CFS.create_messages(
            (
                'Mind Your Route',
            )
        )
def func0(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 7



## code for event 1 ::  
msg1 = CFS.create_messages(
            (

            )
        )
def func1(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 7



## code for event 2 ::  
msg2 = CFS.create_messages(
            (
                'Getting Lost?',
                'Take the help of the Blue Arrow'
            )
        )
def func2(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 7



## code for event 3 ::  
msg3 = CFS.create_messages(
            (
                
            )
        )
def func3(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg3), gameObj.fps * 7



## code for event 4 ::  
msg4 = CFS.create_messages(
            (
                
            )
        )
def func4(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg4), gameObj.fps * 7



## code for event 5 ::  
msg5 = CFS.create_messages(
            (
                'One more to go!',
            )
        )
def func5(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg5), gameObj.fps * 7



## code for event 6 ::  
msg6 = CFS.create_messages(
            (
                'Event 6 just got triggered',
                'This is automatic generation of message'
            )
        )
def func6(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg6), gameObj.fps * 7

