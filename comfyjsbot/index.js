var mysql = require('mysql')
var ComfyJS = require("comfy.js")

require('dotenv').config()

var pool = mysql.createPool({
    connectionLimit : 10,
    host: "127.0.0.1",
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASSWORD,
    database: process.env.MYSQL_DB
})

var logEvent = ( ev_type, ev_cmd, ev_msg, ev_extra ) => {
    if (ev_cmd.length > 254) return;
    if (ev_msg.length > 254) return;
    if (ev_extra.length > 2046) return;

    let sql = "INSERT INTO EVENTS (ev_type, ev_cmd, ev_msg, ev_extra) VALUES ('" + 
        ev_type + "', '" + ev_cmd + "', '" + ev_msg + "', '" + ev_extra + "')"
    

    pool.getConnection( (err, connection) => {
        connection.query( 'START TRANSACTION', (err, rows) => {
            connection.query( sql, (err, rows) => {
                connection.query( 'COMMIT', (err, rows) => {
                    connection.release()
                })
            })
        })
    })
}

ComfyJS.onCommand = ( user, cmd, msg, flags, extra ) => {
    logEvent("COMMAND", cmd, msg, JSON.stringify({user:user, flags:flags, extra:extra}))
}

ComfyJS.onChat = ( user, msg, flags, self, extra ) => {
    if ( flags.customReward && extra.customRewardId === "043d4a49-8e04-4a7c-97d3-9231991ccf65" ) {
        logEvent("JOINREALM", "", msg, JSON.stringify({user: user, flags: flags, extra:extra}))
    } else if ( flags.customReward ) {
        logEvent("CUSTOMREWARD", "", msg, JSON.stringify({user: user, flags: flags, extra:extra}))
    } else {
        logEvent("NORMALCHAT", "", msg, JSON.stringify({user: user, flags: flags, extra:extra}))
    }
}

ComfyJS.onRaid = ( user, viewers, extra ) => {
    logEvent("RAID", "", "", JSON.stringify({user:user, viewers:viewers, extra:extra}))
}

ComfyJS.onCheer = ( user, msg, bits, flags, extra ) => {
    logEvent("CHEER", "", msg, JSON.stringify({user:user, bits:bits, flags:flags, extra:extra}))
}

ComfyJS.onSub = ( user, msg, subTierInfo, extra ) => {
    logEvent("SUB", "", msg, JSON.stringify({user:user, subTierInfo:subTierInfo, extra:extra}))
}

ComfyJS.onResub = ( user, msg, streamMonths, cumulativeMonths, subTierInfo, extra ) => {
    logEvent("RESUB", "", msg, JSON.stringify({user:user, streamMonths:streamMonths, 
            cumulativeMonths:cumulativeMonths, subTierInfo:subTierInfo, extra:extra}))
}

ComfyJS.onSubGift = ( gifterUser, streakMonths, recipientUser, senderCount, subTierInfo, extra ) => {
    logEvent("GIFTSUB", "", "", JSON.stringify({gifterUser:gifterUser, streakMonths:streakMonths, 
            recipientUser:recipientUser, senderCount:senderCount, subTierInfo:subTierInfo, extra:extra}))
}

ComfyJS.onSubMysteryGift = ( gifterUser, numOfSubs, senderCount, subTierInfo, extra ) => {
    logEvent("MYSTERYSUB", "", "", JSON.stringify({gifterUser:gifterUser, numOfSubs:numOfSubs, 
            senderCount: senderCount, subTierInfo: subTierInfo, extra:extra}))
}

ComfyJS.onGiftSubContinue = ( user, sender, extra ) => {
    logEvent("CONTINUESUB", "", "", JSON.stringify({user:user, sender:sender, extra:extra}))
}

ComfyJS.Init( process.env.TWITCH_USER )
