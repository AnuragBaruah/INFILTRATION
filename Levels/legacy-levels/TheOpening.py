import pygame
from Levels import commonfunctions as CFS

## script for mission TheOpening


bgm = CFS.sound_loader('./sounds/music/bass.wav')

## code for event 0 ::  
msg0 = CFS.create_messages(
            (
                'Welcome to INFILTRATION', 'Use W to move towards the mouse pointer', 
                'and S to move away', 'Take the help of the blue arrow to navigate to the green Checkpoints'
            )
        )
def func0(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    levelObj.player.knife_equiped = False
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 10



## code for event 1 ::  
msg1 = CFS.create_messages(
            (
                'You have reached the 1st checkpoint', 
                'The mission is cleared when all the checkpoints are covered in order'
            )
        )
def func1(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 10



## code for event 2 ::  
msg2 = CFS.create_messages(
            (
                'Beware of the ROBOT enemies',
                'They constantly move to and fro between two fixed points',
                'and attack you on touch',
                'Your health is displayed on the top right'
            )
        )
def func2(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg2), gameObj.fps * 10



## code for event 3 ::  
msg3 = CFS.create_messages(
            (
                'Event 3 just got triggered',
                'This is automatic generation of message'
            )
        )
def func3(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    gameObj.music_channel.stop()
    levelObj.player.knife_equiped = False
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg3), gameObj.fps * 10

