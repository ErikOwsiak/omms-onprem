
let realtimeMonitorTimerIDsArr = [];
let MINUTE = 60000;


var realtimeMonitor = {

   /* - - */
   minuteFreq: 6,
   streamTbl: null,
   meterDBID: null,
   keepTicking: true,
   callback: null,

   /* - - */
   tick() {
      /* - - */
      if (realtimeMonitor.isStreamFrameLoaded()) {
         /* read from radio buttons */
         let selector = "#appViewport input[name=\"_streamType\"]:checked", 
            radio = $(selector),
            radioID = $(radio).attr("id");
         /* - - */
         let restapi = new restAPI();
         if (radioID != "__histogram") {
            restapi.getLastReading(radioID
               , realtimeMonitor.meterDBID
               , realtimeMonitor.tack);
         } else {
            /*restapi.getHistogramData(realtimeMonitor.meterDBID
               , realtimeMonitor.tack);*/
            let hrs = $("#histoHrs").val();
            restapi.getHistogramData_v1(hrs, realtimeMonitor.meterDBID
               , realtimeMonitor.tack); 
         }
         /* - - */
      } else {
         realtimeMonitor.clearTimers();
      }
   },

   tack(jobj) {
      try {
         /* - - */
         if (!realtimeMonitor.isStreamFrameLoaded()) {
            realtimeMonitor.clearTimers();  
            return;
         }
         /* - - */
         realtimeMonitor.clearTimers();
         let timeout = (MINUTE / realtimeMonitor.minuteFreq),
            timerID = setTimeout(realtimeMonitor.tick, timeout);
         realtimeMonitorTimerIDsArr.push(timerID);
         /* -- so check if the last clicked table stream is the same as last comming 
            data packet as it could be from a previous table stream */
         let selector = "#appViewport input[name=\"_streamType\"]:checked", 
            currentTbl = $(selector).attr("id");
         if (jobj["streamTbl"] != currentTbl)
            return;
         /* - - */
         if (realtimeMonitor.callback != null)
            realtimeMonitor.callback(jobj);
         /* - - */
      } catch(e) {
         alert(e);
      }
   },

   isStreamFrameLoaded() {
      let boolval = ($("#appViewport").find("#streamFrame").length == 1);
      if (boolval)
         $("#streamSelector").removeAttr("disabled");
      else
         $("#streamSelector").attr("disabled", "true");
      return boolval;
   },

   clearTimers() {
      realtimeMonitorTimerIDsArr.forEach(timerID => {
            clearTimeout(timerID);
         });
      /* - - */
      realtimeMonitorTimerIDsArr = [];
   },

   stop() {
      app.lastClickedMeter = null;
      realtimeMonitor.keepTicking = false;
   },

   on() {
      realtimeMonitor.keepTicking = true;
   },

   off() {
      app.lastClickedMeter = null;
      realtimeMonitor.keepTicking = false;
   }

};
