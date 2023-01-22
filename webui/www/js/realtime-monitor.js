
_omms.realtimeMonitorTimerIDsArr = [];
_omms.MINUTE = 60000;


_omms.realtimeMonitor = {

   /* - - */
   minuteFreq: 6,
   streamTbl: null,
   meterDBID: null,
   keepTicking: true,
   callback: null,

   /* - - */
   tick() {
      /* - - */
      if (_omms.realtimeMonitor.isStreamFrameLoaded()) {
         /* read from radio buttons */
         let selector = "#appViewport input[name=\"_streamType\"]:checked", 
            radio = $(selector),
            radioID = $(radio).attr("id");
         /* - - */
         let restapi = new restAPI();
         if (radioID != "__histogram") {
            restapi.getLastReading(radioID
               , _omms.realtimeMonitor.meterDBID
               , _omms.realtimeMonitor.tack);
         } else {
            /*restapi.getHistogramData(realtimeMonitor.meterDBID
               , realtimeMonitor.tack);*/
            let hrs = $("#histoHrs").val();
            restapi.getHistogramData_v1(hrs, _omms.realtimeMonitor.meterDBID
               , _omms.realtimeMonitor.tack); 
         }
         /* - - */
      } else {
         _omms.realtimeMonitor.clearTimers();
      }
   },

   tack(jobj) {
      try {
         /* - - */
         if (!_omms.realtimeMonitor.isStreamFrameLoaded()) {
            _omms.realtimeMonitor.clearTimers();  
            return;
         }
         /* - - */
         _omms.realtimeMonitor.clearTimers();
         let timeout = (MINUTE / _omms.realtimeMonitor.minuteFreq),
            timerID = setTimeout(_omms.realtimeMonitor.tick, timeout);
            _omms.realtimeMonitorTimerIDsArr.push(timerID);
         /* -- so check if the last clicked table stream is the same as last comming 
            data packet as it could be from a previous table stream */
         let selector = "#appViewport input[name=\"_streamType\"]:checked", 
            currentTbl = $(selector).attr("id");
         if (jobj["streamTbl"] != currentTbl)
            return;
         /* - - */
         if (_omms.realtimeMonitor.callback != null)
            _omms.realtimeMonitor.callback(jobj);
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
      _omms.realtimeMonitorTimerIDsArr.forEach(timerID => {
            clearTimeout(timerID);
         });
      /* - - */
      _omms.realtimeMonitorTimerIDsArr = [];
   },

   stop() {
      _omms.app.lastClickedMeter = null;
      _omms.realtimeMonitor.keepTicking = false;
   },

   on() {
      _omms.realtimeMonitor.keepTicking = true;
   },

   off() {
      _omms.app.lastClickedMeter = null;
      _omms.realtimeMonitor.keepTicking = false;
   }

};
