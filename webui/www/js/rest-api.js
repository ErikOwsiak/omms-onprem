
/*
   fetch('http://example.com/movies.json')
   .then(response => response.json())
   .then(data => console.log(data));
   http://85.222.109.238:4080/
*/

class restAPI {

   lastScannedStreamTbl = null;

   constructor(host = "", port = 0) {
      /* -- */
      this.host = host;
      this.port = port;
      this.restURL = ``;
      this.getMetersUrl = "/api/get/meters";
      this.urlGetElcRoomMeters = "/api/get/elc-room-meters";
      this.urlGetElcRoomMetersActive = "/api/get/elc-room-meters-active";
      this.getLastReadingUrl = "/api/get/lastreading";
      this.getOrgUrl = "/api/get/org";
      this.putConfigUrl = "/api/put/config";
      this.delConfigUrl = "/api/del/config";
      this.getDataUrl = "/api/get/config";
      /* reports urls */
      this.getClientsUrl = "/api/get/clients";
      this.getCircuitsUrl = "/api/get/circuits";
      this.getReportUrl = "/api/get/report";
      this.getHistogramUrl = "/api/get/histogram";
      this.getHistogramUrl_v1 = "/api/v1/get/histogram";
      this.getTableInfoUrl = "/api/get/table-info";
      /* clt circuits */
      this.getCltCircuitsUrl = "/api/get/clt-circuits";
      this.putCltCircuitsUrl = "/api/put/clt-circuits";
      this.delCltCircuitsUrl = "/api/del/clt-circuits";
      /* table quries */
      this.getTableUrl = "/api/get/table";
      this.getLisReportstUrl = "/api/get/list-reports";
      // /api/get/meters
      this.getClientMetersUrl = "/api/get/meters";
      this.getClientCircuitHistoryUrl = "/api/get/clt-cir-history";
      this.getCltCircuitsUrlv1 = "/api/get/client_circuits";
      this.getClinetKWhrsUrl = "/api/get/client_kwhrs";
   }

   getOrg(callback = undefined) {
      $.get(this.getOrgUrl, callback)
   }

   getMeters(flags = 0, callback = undefined) {
      let url = `${this.getMetersUrl}/${flags}`
      $.get(url, callback)
   }

   getElcRoomMeters(entityTag, callback = undefined) {
      let url = `${this.urlGetElcRoomMeters}/${entityTag}`
      $.get(url, callback)
   }

   getElcRoomMetersActive(entag, callback) {
      let url = `${this.urlGetElcRoomMetersActive}/${entag}`;
      $.get(url, callback)
   }

   /* http://85.222.109.238:4080/api/get/lastreading/kwhrs/1001 */
   getLastReading(tbl, dbid, callback) {
      restAPI.lastScannedStreamTbl = tbl;
      let url = `${this.getLastReadingUrl}/${tbl}/${dbid}`
      $.get(url, callback);  
   }

   upsertConfigTable(data, callback) {
      let j = JSON.stringify(data), 
         d = encodeURIComponent(j),
         url = `${this.putConfigUrl}/${d}`;
      /* - - */
      $.post(url, callback);
   }

   deleteConfigRow(data, callback) {
      let j = JSON.stringify(data), 
         d = encodeURIComponent(j),
         url = `${this.delConfigUrl}/${d}`;
      /* - - */
      $.post(url, callback);
   }

   getClients(__cb__) {
      $.get(this.getClientsUrl, (jarr) => {
            console.log(jarr);
            if (jarr) {
               _omms.app.clients = {};
               _omms.app.clients.dts = Date();
               _omms.app.clients.jarr = jarr;
            }
            /* -- */
            __cb__(_omms.app.clients.jarr);
         });
   }

   getCircuits(callback) {
      $.get(this.getCircuitsUrl, callback);
   }

   getTable(tbl, args, callback) {
      if (args == "" || args == null)
         args = ""
      else
         args += "/"
      /* - - */
      let url = `${this.getTableUrl}/${tbl}` + args   
      $.get(url, callback);
   }

   getClientCircuits(callback) {
      $.get(this.getCltCircuitsUrl, callback);
   }

   getDatalist(url, callback) {
      $.get(url, callback);
   }

   /* data = {"aggreateOn": this.aggreateOn, "startDate": this.startDate
      , "endDate": this.endDate, "totalOnly":  this.totalOnly}; */
   getReport_kWhrsByClient(clt, data, callback) {   
      /* - - */
      let sort = function(itemA, itemB) {
            let spA = itemA[4].toUpperCase(),
               spB = itemB[4].toUpperCase();
            /* - - */
            if (spA < spB)
               return -1;
            /* - - */
            if (spA > spB)
               return 1;
            /* - - */
            return 0;
         };
      /* - - */
      let clttag = clt.client_tag,
         sdate = data.startDate, edate = data.endDate, 
         url = `${this.getReportUrl}/client-kwhrs/${clttag}/${sdate}/${edate}`;
      /* make the call */
      $.get(url, function(jarr) {
            if (_omms.app.kwhrsReport == undefined) {   
               _omms.app.kwhrsReport = {"dts": new Date(), "jarrs": []};
            } else {
               /* sort jarr by client space here */
               jarr.sort(sort);
               _omms.app.kwhrsReport.jarrs.push({"clttag": clttag, "jarr": jarr});
               callback(jarr);
            }
         });
      /* - - */
   }

   getHistogramData(meterDBID, callback) {
      let url = `${this.getHistogramUrl}/${meterDBID}`;
      $.get(url, callback);
   }

   getHistogramData_v1(hrs, meterDBID, callback) {
      let url = `${this.getHistogramUrl_v1}/${hrs}/${meterDBID}`;
      $.get(url, callback);
   }

   getTableInfo(tbl, callback) {
      /* - - */
      if (_omms.app.tblInfos == undefined)
      _omms.app.tblInfos = {};
      if (tbl in _omms.app.tblInfos) {
         callback(_omms.app.tblInfos[tbl], tbl);
         return;
      }
      /* - - */
      let url = `${this.getTableInfoUrl}/${tbl}`;
      $.get(url, function(jarr) {
         _omms.app.tblInfos[tbl] = jarr;
            callback(jarr, tbl);
         });
      /* - - */
   }

   getKwhrsReportList(__cb__) {
      $.get(this.getLisReportstUrl, (res) => {
            if (__cb__) {
               __cb__(res);
            } else {
               console.log(res);
            }
         });
   }

   getClientMeters(dbid, __cb__) {
      /* -- */
      let url = `${this.getClientMetersUrl}?cltrowid=${dbid}`;
      $.get(url, (res) => {
            if (__cb__) {
               __cb__(res);
            } else {
               console.log(res);
            }   
         });
      /* -- */
   }

   getClientCircuitHistory(__cb__) {
      let _this = this;
      $.get(this.getClientCircuitHistoryUrl, (res) => {
            _this.tryCallCallback(res, __cb__);
         });   
   }

   getClientCircuitsV1(clttag, __cb__) {
      let _this = this, 
         url = `${this.getCltCircuitsUrlv1}?clttag=${clttag}`;
      $.get(url, function(jsarr) {
            _this.tryCallCallback(jsarr, __cb__);
         });
   }

   getClinetKWhrs(dts, cirs, __cb__) {
      let _this = this, 
         url = `${this.getClinetKWhrsUrl}?dts=${dts}&cirs=${cirs}`;
      $.get(url, function(jsarr) {
            _this.tryCallCallback(jsarr, __cb__);
         });
   }

   tryCallCallback(resp, __cb__) {
      if (__cb__)
         __cb__(resp);
      else
         console.log(resp);
   }
};
