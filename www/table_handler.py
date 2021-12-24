import json

class TableHandler():
    ev_priority = {
        "RAID": 12,
        "CHEER": 10,
        "SUB": 10,
        "RESUB": 10,
        "GIFTSUB": 10,
        "MYSTERYSUB": 10,
        "CONTINUESUB": 7,
        "FOLLOW": 6,
        "GAMECHANGE":5,
        "CLEAR":4,
        "COMMAND": 3
        "JOINREALM": 2,
        "CUSTOMREWARD": 2,
        "NORMALCHAT": 0
    }

    def get_event(self, db):
        # [(id, ev_type, ev_extra, importance)]
        res = db.query("SELECT * FROM P_QUEUE ORDER BY importance DESC")
        if len(res) == 0:
            return
        ev = res[0]
        ev = (ev[0], ev[1], json.loads(ev[2]), ev[3])

        if self.should_clear(ev):
            db.execute(f"DELETE FROM P_QUEUE WHERE 1=1")
            return
        
        db.execute(f"DELETE FROM P_QUEUE WHERE id={ev[0]}")
        
        return ev
    
    def process_events(self, db):
        # [(id, ev_type, ev_extra)]
        res = db.query("SELECT * FROM EVENTS")

        latest_entry = 0
        for x in res:
            ev_type = x[1]
            if x[0] > latest_entry:
                latest_entry = x[0]
            if ev_type in self.ev_priority:
                sql = "INSERT INTO P_QUEUE (ev_type, ev_extra, importance) VALUES " + \
                    f"('{ev_type}', '{x[2]}', {self.ev_priority[ev_type]})"
                db.query(sql)

        db.execute(f"DELETE FROM EVENTS WHERE id <= {latest_entry}")

    # event = (id, ev_type, ev_extra, importance)
    def should_clear(self, event):
        return (event[1] == "COMMAND" and 
            event[2]['command'].lower() == "clear" and
            (event[2]['flags']['mod'] or event[2]['flags']['broadcaster']))
