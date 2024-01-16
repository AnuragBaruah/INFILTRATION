import pygame
from Levels import commonfunctions as CFS

## script for mission GetKnife

bgm = CFS.sound_loader('./sounds/music/bassanddrum.wav')

## code for event 0 ::  
msg0 = CFS.create_messages(
            (
                'THE TUNNEL OF DEATH',
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
                'Great! Now you have a Knife',
                'Press RightMouseButton to use knife',
                'You can damage enemies by clicking mouse when the enemy overlaps with you'
            )
        )
def func1(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    levelObj.player.knife_equiped = True
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg1), gameObj.fps * 10



## code for event 2 ::  
msg2 = CFS.create_messages(
            (
                
            )
        )
def func2(gameObj, levelObj = None) -> tuple['function', tuple, int]:
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
    CFS.play_sound(gameObj.mission_pass_channel)
    gameObj.music_channel.stop()
    return CFS.render_messages, (gameObj.screen, msg3), gameObj.fps * 10

