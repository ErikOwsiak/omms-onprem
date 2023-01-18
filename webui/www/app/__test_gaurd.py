
import core.guard as guard


c = "openbms-session=f2c584968e824911af89e406fe4f4999; Expiers=Wed, 03-Nov-2021 00:06:28 GMT;"
g: guard.guard = guard.guard()
robj = g.check_session(c)
print(robj)
