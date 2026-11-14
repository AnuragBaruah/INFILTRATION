from Levels import commonfunctions as CFS

bgm = CFS.sound_loader('./sounds/music/all.wav')

_lines = [
    ('This route spans nine sectors. Commit to each crossing before entering it.',),
    ('The blue arrow points to the marker, not to a safe path.',),
    ('Use the outer wall to keep your bearings when ghosts close in.',),
    ('A bomb clears space, but you must leave its marked area first.',),
    ('The next marker lies across the lower route. Do not cut through the center.',),
    ('The path turns back through the middle sectors. Check the arrow after each turn.',),
    ('Final sector. Keep one retreat lane open until you reach extraction.',),
]
_messages = [CFS.create_messages(line) for line in _lines]

def _event(gameObj, index, levelObj, stop_music=False):
    if index == 0:
        levelObj.player.knife_equiped = False
        gameObj.music_channel.play(bgm, -1)
    if stop_music:
        gameObj.music_channel.stop()
    CFS.play_sound(gameObj.mission_pass_channel)
    return CFS.render_messages, (gameObj.screen, _messages[index]), gameObj.fps * 8

def func0(gameObj, levelObj=None): return _event(gameObj, 0, levelObj)
def func1(gameObj, levelObj=None): return _event(gameObj, 1, levelObj)
def func2(gameObj, levelObj=None): return _event(gameObj, 2, levelObj)
def func3(gameObj, levelObj=None): return _event(gameObj, 3, levelObj)
def func4(gameObj, levelObj=None): return _event(gameObj, 4, levelObj)
def func5(gameObj, levelObj=None): return _event(gameObj, 5, levelObj)
def func6(gameObj, levelObj=None): return _event(gameObj, 6, levelObj, stop_music=True)
