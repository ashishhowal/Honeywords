# Because I love making custom logger methods :)

_DEBUG = True

def dlog(text):
    if _DEBUG == False:
        return
    YELLOW = '\033[33m'
    WHITE = '\033[37;0m'
    print(YELLOW + "[ DEBUG\t]________" + str(text) + WHITE)
    return