
from webui.app.core.pagebuff import pageBuffer


pb: pageBuffer = pageBuffer()
rv = pb.load("login")
print(rv)
