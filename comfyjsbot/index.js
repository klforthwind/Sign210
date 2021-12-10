var mysql = require('mysql')
var ComfyJS = require("comfy.js")

require('dotenv').config()

var pool  = mysql.createPool({
    connectionLimit : 10,
    host: "127.0.0.1",
    user: process.env.MYSQL_USER,
    password: process.env.MYSQL_PASSWORD,
    database: process.env.MYSQL_DB
})

var logEvent = ( ev_type, ev_extra ) => {
    pool.getConnection(function(err, connection) {
        if (err) {console.log(err)}
        if (ev_extra.length < 127) {
            var sql = "INSERT INTO EVENTS (ev_type, ev_extra) VALUES ('" + ev_type + "', '" + ev_extra + "')"
            connection.query( sql, function(err, rows) {
                connection.release()
            })
        }
        
    })
}

ComfyJS.onCommand = ( user, command, message, flags, extra ) => {
    logEvent("COMMAND", JSON.stringify({user:user, command:command, message:message, flags:flags, extra:extra}))

//     if( flags.broadcaster && command === "test" ) {
//         console.log( "!test was typed in chat" );
//     }
}

ComfyJS.onChat = ( user, message, flags, self, extra ) => {
    // logEvent("", "")
    // if ( flags.broadcaster && "followed" in message ) {
    //     logEvent("FOLLOW", user.split(" ")[0])
    // } else 
    if ( flags.customReward && extra.customRewardId === "043d4a49-8e04-4a7c-97d3-9231991ccf65" ) {
        logEvent("JOINREALM", JSON.stringify({user: user, message: message, flags: flags, extra:extra}))
    } else if ( flags.customReward ) {
        logEvent("CUSTOMREWARD", JSON.stringify({user: user, message: message, flags: flags, extra:extra}))
    } else {
        logEvent("NORMALCHAT", JSON.stringify({user: user, message: message, flags: flags, extra:extra}))
    }
}

ComfyJS.onRaid = ( user, viewers, extra ) => {
    logEvent("RAID", JSON.stringify({user:user, viewers:viewers, extra:extra}))
}

ComfyJS.onCheer = ( user, message, bits, flags, extra ) => {
    logEvent("CHEER", JSON.stringify({user:user, message:message, bits:bits, flags:flags, extra:extra}))
}

ComfyJS.onSub = ( user, message, subTierInfo, extra ) => {
    logEvent("SUB", JSON.stringify({user:user, message:message, subTierInfo:subTierInfo, extra:extra}))
}

ComfyJS.onResub = ( user, message, streamMonths, cumulativeMonths, subTierInfo, extra ) => {
    logEvent("RESUB", JSON.stringify({user:user, message:message, streamMonths:streamMonths, 
            cumulativeMonths:cumulativeMonths, subTierInfo:subTierInfo, extra:extra}))
}

ComfyJS.onSubGift = ( gifterUser, streakMonths, recipientUser, senderCount, subTierInfo, extra ) => {
    logEvent("GIFTSUB", JSON.stringify({gifterUser:gifterUser, streakMonths:streakMonths, 
            recipientUser:recipientUser, senderCount:senderCount, subTierInfo:subTierInfo, extra:extra}))
}

ComfyJS.onSubMysteryGift = ( gifterUser, numOfSubs, senderCount, subTierInfo, extra ) => {
    logEvent("MYSTERYSUB", JSON.stringify({gifterUser:gifterUser, numOfSubs:numOfSubs, 
            senderCount: senderCount, subTierInfo: subTierInfo, extra:extra}))
}

ComfyJS.onGiftSubContinue = ( user, sender, extra ) => {
    logEvent("CONTINUESUB", JSON.stringify({user:user, sender:sender, extra:extra}))
}

ComfyJS.Init( "jjdb210" )
