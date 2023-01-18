
/*
   1. pull all clients
   2. run sum on all meters linked to a client
   * client should be tagged with org entag

   notes:
      ^(get)/(report)/(client-kwhrs)/([a-zA-Z0-9\-]{4,32})$

*/

class kWhrsReport {

   /*
      statics
   */

   static getReportHtmlPreview(type) {
      switch(type) {
         case "client_meter":
            return kWhrsReport.getClientMeterReportHtmlPreview();
         case "client_space":
            return kWhrsReport.getClientSpacesReportHtmlPreview();
         default:
            break;
      }
   }


   static getClientMeterReportHtmlPreview() {
      /* - - */
      let out = [];
      if (!app.lastReports.clientMeters.length)
         return out;
      /* - - */
      let onreport = function(rpt) {
            for (let midx in rpt.lnsArr) {
                  let meter = rpt.lnsArr[midx],
                     kwhs = meter.kwhs.toFixed(2),
                     buff = html.kWhPreviewTableRow(meter.clt.client_tag
                        , meter.clt.client_name, meter.space, meter.ctags, kwhs);
               /* - - */
               out.push(buff);
            }
         };
      /* - - */
      app.lastReports.clientMeters.forEach(onreport);
      /* - - */
      return html.kWhPreviewTable(out.join(""));
   }

   static getClientSpacesReportHtmlPreview() {
      let out = [];
      if (!app.lastReports.clientSpaces.length)
         return out;
      /* - - */
      let onreport = function(rpt) {
            for (let spaceID in rpt.lnsObj) {
                  let buff = "", 
                     space = rpt.lnsObj[spaceID];
                  if ((space == null) || (space == undefined)) {
                     console.log(`no space for spaceID: ${spaceID}`);
                     continue;
                  } else {
                     try {
                        let kwhs = space.kwhs.toFixed(2);
                        buff = html.kWhPreviewTableRow(space.clt.client_tag
                           , space.clt.client_name, space.space, space.ctags, kwhs);
                     } catch(e) {
                        console.log(`Error for spaceID: ${spaceID}`);
                        console.log(e);
                     }
                  }
               /* - - */
               if (buff != "")
                  out.push(buff);
            }
         };
      /* - - */
      app.lastReports.clientSpaces.forEach(onreport);
      /* - - */
      return html.kWhPreviewTable(out.join(""));
   }

   
   /*
      object
   */

   constructor(api, aggreateOn, startDate, endDate, totalOnly) {
      /* - - */
      this.restApi = api;
      this.aggreateOn = aggreateOn;
      this.startDate = startDate;
      this.endDate = endDate;
      this.totalOnly = totalOnly;
      /* - - */
   }

   /*
      start running report
   */
   run() {
      /* -- clear cache -- */
      app.lastReports.clientMeters = [];
      app.lastReports.clientSpaces = [];
      /* - - */
      let __this = this,
         data = {"aggreateOn": this.aggreateOn, "startDate": this.startDate
            , "endDate": this.endDate, "totalOnly":  this.totalOnly};
      /* -- this gets all the clients from the server -- */
      this.restApi.getClients((res) => {
            $("#kWhrsRptFrame .kwhrs-rpt-body").html("");
            __this.onGetClients(res, data);
         });
      /* - - */
   }

   /*
      this runs on client list from the server
      data: holds aggreateOn
   */
   onGetClients(resClients, data) {
      /* - - */
      let __this = this,
         callCounter = 0;
      /* - - */
      let runReportPerClient = function(clt) {
            /* load kwh from the server per client */
            __this.restApi.getReport_kWhrsByClient(clt, data, function(res) {
                  gui.kWhrsReportLineAdd(clt, data, res);
                  if (resClients.length == ((callCounter++) + 1))
                     app.lightBoxedPane.onClickX();
               });
         };
      /* -- resClients is a list of clients -- */ 
      $(resClients).each(function(idx) {
            let client = resClients[idx];
            runReportPerClient(client);
         });
      /* - - */
   }

   saveCSV(filename) {
      /* - - */
      let join = function(elAll) {
            let out = [];
            elAll.forEach((i, _) => {
                  out.push(i.innerText);
               });
            /* - - */
            return out.join("; ");
         };
      /* - - */
      let lines = [],
         selector = "#lbPaneBody table#tblReportPreview",
         table = document.querySelector(selector),
         trAll = table.querySelectorAll("tr");
      /* - - */
      trAll.forEach((tr, idx) => {
            if (idx == 0) {
               let thAll = tr.querySelectorAll("th");
               lines.push(join(thAll));
            } else {
               let tdAll = tr.querySelectorAll("td");
               lines.push(join(tdAll));
            }
         });
      /* - - */
      let tmp = window.document.createElement("a"),
         blob = new Blob([lines.join("\n")], {type: "text/csv"});
      tmp.href = window.URL.createObjectURL(blob);
      tmp.download = filename;
      /* -- Append anchor to body -- */
      document.body.appendChild(tmp);
      tmp.click();
      /* -- Remove anchor from body -- */
      document.body.removeChild(tmp);
   }

};
