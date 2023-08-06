from writema.writema import Writema, WritemaFloatTypes, WritemaTypes

if __name__ == '__main__':
    w = Writema()  # this is to make a certain test not be angry
    wm = WritemaTypes.__members__  # so is this
    wf = WritemaFloatTypes.__members__  # yeah
    print("Hello there. I think you're running the wrong file!")
