
class SystemOverview {

   static __this__ = null;
   static TIMEOUT = 30000;

   constructor(divID) {
      this.divID = divID;
      SystemOverview.__this__ = this;
   }

   tick() {
      const selector = "#appViewport #systemOverview";
      if ($(selector).length == 0) {
         console.log("--- [stopping overview tic/tack] ---");
         return;
      }
      /* -- else -- */
      let url = "ui/api/get/overview";
      $.get(url, SystemOverview.__this__.tack);
   }

   tack(jsobj) {
      /* -- */
      console.log(jsobj);
      if (!SystemOverview.__this__.isSysOverviewLoaded())
         return;
      /* -- else -- */
      setTimeout(SystemOverview.__this__.tick
         , SystemOverview.TIMEOUT);
      /* -- */
      if (jsobj.error == undefined)
         return;
      /* -- */
      SystemOverview.__this__.jsobj = jsobj;
      $("#sunClock #tsSunrise .txt").html(jsobj.sunrise);
      $("#sunClock #tsSunset .txt").html(jsobj.sunset);
      /* -- */
      let ontimeCnt = jsobj.ontime.length;
      $("#spathsCounts #ontime").html(`OnTime: ${ontimeCnt}`);
      let late3hCnt = jsobj.late_3h.length;
      $("#spathsCounts #late_3h").html(`Late 3h ~ 6h: ${late3hCnt}`);
      let late6hCnt = jsobj.late_6h.length;
      $("#spathsCounts #late_6h").html(`Late > 6h: ${late6hCnt}`);
      let missingCnt = jsobj.missing.length;
      $("#spathsCounts #missing").html(`Missing: ${missingCnt}`);
      let badReadsCnt = jsobj.bad_reads.length;
      $("#spathsCounts #bad_reads").html(`Bad Reads: ${badReadsCnt}`);
      /* -- */
      $("div.read-stat").off().on("click", function() {
            $("#rightCol").html("");
            let btn_id = this.id, arr = SystemOverview.__this__.jsobj[btn_id];
            if (Array.isArray(arr)) {
               arr.forEach((i) => {
                     let _buff = `<div class="lst-item"><div>${i}</div></div>`;
                     $("#rightCol").append(_buff);
                  });
               /* -- */
            }
            /* -- */
            $("div.read-stat").removeClass("clicked");
            $(this).addClass("clicked");
         });
      /* -- */
   }

   isSysOverviewLoaded() {
      return ($("#systemOverview").length == 1);
   }

};
