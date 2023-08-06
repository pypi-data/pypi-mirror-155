from threadsnake.core import *

set_log_config(LogLevel.ALL)
badge_async('threadsnake 0.0.15', title='version')

app = Application(get_port(8088))

app.use_router(routes_to('router'), '/router/')
app.wait_exit()