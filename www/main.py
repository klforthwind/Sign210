from table_handler import *
from db_conn import *
from lights import *
from show import *
import time

UPDATES_WAIT_TIME_SEC = 300

table = TableHandler()
pixels = Lights()
show = Show()

db = DBConn()
db.connect()

t_end = time.time() + UPDATES_WAIT_TIME_SEC
while time.time() < t_end:

    # process EVENTS table
    table.process_events(db)

    # get event from P_QUEUE table
    ev = table.get_event(db)

    # run event
    show.run(ev, db, pixels)

db.disconnect()
