from table_handler import *
from db_conn import *
from lights import *
from show import *
import time

UPDATES_WAIT_TIME_SEC = 600

table = TableHandler()
pixels = Lights()
show = Show()

db = DBConn()

t_end = time.time() + UPDATES_WAIT_TIME_SEC
while time.time() < t_end:
    time.sleep(0.2)

    db.connect()

    # Process EVENTS table
    table.process_events(db)

    # Get event from P_QUEUE table
    ev = table.get_event(db)

    # Run event
    show.run(ev, db, pixels)

    db.disconnect()
