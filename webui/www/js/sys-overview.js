

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
      let url = "/api/v1/get/overview"
      $.get(url, SystemOverview.__this__.tack);
   }

   tack(jarr) {
      /* -- */
      if (!SystemOverview.__this__.isSysOverviewLoaded())
         return;
      /* -- else -- */
      setTimeout(SystemOverview.__this__.tick
         , SystemOverview.TIMEOUT);
      /* calc if the ping overdue */
      let isoverdue = function(ping, maxMinutes) {
            try {
               let msMin = 60000, 
                  nowDts = Date.now(),
                  /* utc time */
                  pingUtcStr = ping[2].trim();
               /* -- go -- */
               /* 2021-12-05 19:04:29.956 */
               let rx = /([\d]{4})-([\d]{2})-([\d]{2})\s{1}([\d]{2}):([\d]{2}):([\d]{2})/gm;
               let m = rx.exec(pingUtcStr);
               let [y, mo, d, h, mn,] = m.slice(1);
               mo = parseInt(mo); d = parseInt(d); h = parseInt(h); 
               let pingDts = Date.UTC(y, --mo, d, h, mn, 0, 0);
               let diff = parseInt((nowDts - pingDts) / msMin);
               return (diff > maxMinutes);
            } catch(e) {
               return false;
            }
         };
      /* -- display info -- */
      let less5 = `<div class="less5">under 5 min.</div>`,
         over5 = `<div class="over5">over 5 min.</div>`,
         hdr = `<div class="ping-status-hdr">Last Ping Status ${over5}${less5}</div>`,
         maxMinutes = 5, late = false, pings = [], htmlArr = [hdr];
      /* on each */
      jarr.forEach(e => {
            try {
               late = isoverdue(e.ping, maxMinutes);
               pings.push(e.ping.push(late));
               htmlArr.push(html.ping(e.ping));
            } catch(e) {
               console.log(e);
            }
         });
      /* -- out -- */
      $("#soPaneBody").html(htmlArr.join(""));
   }

   isSysOverviewLoaded() {
      return ($("#systemOverview").length == 1);
   }

};
