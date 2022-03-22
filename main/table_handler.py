from collections import defaultdict
from extra_funcs import *
import json

class TableHandler():
    ev_priority = defaultdict(
        lambda: 0, {
        "ALLCLEAR": 13,
        "RAID": 12,
        "CHEER": 10,
        "SUB": 10,
        "RESUB": 10,
        "GIFTSUB": 10,
        "MYSTERYSUB": 10,
        "CONTINUESUB": 7,
        "FOLLOW": 6,
        "GAMECHANGE": 5,
        "CLEAR": 4,
        "COMMAND": 3,
        "JOINREALM": 2,
        "CUSTOMREWARD": 2,
        "NORMALCHAT": 0
    })

    def get_event(self, db):
        """Get event from P_QUEUE table."""
        res = db.query("SELECT id, ev_type, ev_cmd, ev_msg, ev_extra, importance FROM P_QUEUE ORDER BY importance DESC")

        if len(res) == 0:
            return
        
        event = list(res[0])
        event[4] = json.loads(event[4])

        clear_cond = "1=1" if self.should_clear(event) else f"id={event[0]}"
        db.execute(f"DELETE FROM P_QUEUE WHERE {clear_cond}")
        return event

    def process_events(self, db):
        """Process events from EVENTS table into P_QUEUE table. Returns 1 on no events."""
        res = db.query("SELECT id, ev_type, ev_cmd, ev_msg, ev_extra FROM EVENTS")

        if len(res) == 0:
            return 1
        
        latest_id = res[len(res)-1][0]

        for row in res:
            ev_type = row[1]
            cmd = row[2].upper()
            is_clear = ev_type == "COMMAND" and cmd in ["ALLCLEAR", "CLEAR"]

            priority_key = cmd if is_clear else ev_type
            priority = self.ev_priority[priority_key]

            sql = "INSERT INTO P_QUEUE (ev_type, ev_cmd, ev_msg, ev_extra, importance) " + \
                f"VALUES ('{ev_type}', '{row[2]}', '{row[3]}', '{row[4]}', {priority})"
            db.execute(sql)

        db.execute(f"DELETE FROM EVENTS WHERE id <= {latest_id}")

    # event = (id, ev_type, ev_extra, importance)
    def should_clear(self, event):
        """Returns whether the P_QUEUE table should be cleared based on current event."""
        return (event[1] == "COMMAND" and 'flags' in event[4] and
            event[2].upper() in ["ALLCLEAR", "CLEAR"] and 
            (event[4]['flags']['mod'] or event[4]['flags']['broadcaster']))
