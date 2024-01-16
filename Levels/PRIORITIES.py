import pygame
from Levels import commonfunctions as CFS

## script for mission PRIORITIES

bgm = CFS.sound_loader('./sounds/music/bassanddrum.wav')

## code for event 0 ::  
msg0 = CFS.create_messages(
            (
                "There's a long way to go",
            )
        )
def func0(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    gameObj.music_channel.play(bgm, -1)
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg0), gameObj.fps * 10



## code for event 1 ::  
msg1 = CFS.create_messages(
            (
                'Just the first one till now',
            )
        )
def func1(gameObj, levelObj = None) -> tuple['function', tuple, int]:
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
                
            )
        )
def func3(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg3), gameObj.fps * 10



## code for event 4 ::  
msg4 = CFS.create_messages(
            (
                
            )
        )
def func4(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg4), gameObj.fps * 10



## code for event 5 ::  
msg5 = CFS.create_messages(
            (
                
            )
        )
def func5(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg5), gameObj.fps * 10



## code for event 6 ::  
msg6 = CFS.create_messages(
            (
                
            )
        )
def func6(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg6), gameObj.fps * 10



## code for event 7 ::  
msg7 = CFS.create_messages(
            (
                
            )
        )
def func7(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg7), gameObj.fps * 10



## code for event 8 ::  
msg8 = CFS.create_messages(
            (
                
            )
        )
def func8(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg8), gameObj.fps * 10



## code for event 9 ::  
msg9 = CFS.create_messages(
            (
                
            )
        )
def func9(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg9), gameObj.fps * 10



## code for event 10 ::  
msg10 = CFS.create_messages(
            (
                'Midway',
            )
        )
def func10(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg10), gameObj.fps * 10



## code for event 11 ::  
msg11 = CFS.create_messages(
            (
                
            )
        )
def func11(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg11), gameObj.fps * 10



## code for event 12 ::  
msg12 = CFS.create_messages(
            (
                
            )
        )
def func12(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg12), gameObj.fps * 10



## code for event 13 ::  
msg13 = CFS.create_messages(
            (
                
            )
        )
def func13(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg13), gameObj.fps * 10



## code for event 14 ::  
msg14 = CFS.create_messages(
            (
                
            )
        )
def func14(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg14), gameObj.fps * 10



## code for event 15 ::  
msg15 = CFS.create_messages(
            (
                
            )
        )
def func15(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg15), gameObj.fps * 10



## code for event 16 ::  
msg16 = CFS.create_messages(
            (
                
            )
        )
def func16(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg16), gameObj.fps * 10



## code for event 17 ::  
msg17 = CFS.create_messages(
            (
                
            )
        )
def func17(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg17), gameObj.fps * 10



## code for event 18 ::  
msg18 = CFS.create_messages(
            (
                
            )
        )
def func18(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg18), gameObj.fps * 10



## code for event 19 ::  
msg19 = CFS.create_messages(
            (
                'One more to go',
            )
        )
def func19(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg19), gameObj.fps * 10



## code for event 20 ::  
msg20 = CFS.create_messages(
            (
                
            )
        )
def func20(gameObj, levelObj = None) -> tuple['function', tuple, int]:
    gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, msg20), gameObj.fps * 10

