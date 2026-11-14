from Levels import commonfunctions as CFS

bgm = CFS.sound_loader('./sounds/music/all.wav')

_lines = [
    ('Start by collecting the nearby charges while you cross the first court.',),
    ('Ghosts pass through walls. Use the corner to make them take the long way.',),
    ('The route doubles back; leave a clear lane behind you.',),
    ('The next cache is on the outer route. Pick it up as you pass.',),
    ('Let the ghosts bunch before planting a charge.',),
    ('The center is exposed. Retreat around the wall before detonating.',),
    ('Final marker. Take the last corner wide and keep moving.',),
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
