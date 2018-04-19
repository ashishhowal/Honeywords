# Because I love making custom logger methods :)

_DEBUG = True

def dlog(text):
    if _DEBUG == False:
        return
    print("[ DEBUG\t]________" + str(text))
    return