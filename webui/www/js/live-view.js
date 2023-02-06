
_omms.liveView = {

   restapi: null,
   client_tag: null,
   clinet_circuits: null,
   server_utcnow: 0,

   init() {
      _omms.liveView.restapi = new restAPI();
      _omms.liveView.restapi.getClients(_omms.liveView.onGetClients);
   },

   run() {
   },

   onGetClients(jsarr) {
      /* -- */
      let selector = "#selCltSelector"
         , _opt = `<option value="" selected> -- set client --</option>`;
      /* -- */
      $(selector).html("")
      $(selector).append(_opt);
      /* -- */
      jsarr.forEach((v, _x, _y) => {
            let [dbid, tag, cltname] = v,
               val = `dbid:${dbid}|tag:${tag}`,
               opt = `<option value="${val}">${cltname}</option>`;
            $(selector).append(opt);
         });
      /* -- */
   },

   onClientSelected(_this) {
      _omms.liveView.client_tag = $(this).val();
      if (_omms.liveView.client_tag == "") {
         _omms.liveView.clinet_circuits = null;
         _omms.liveView.monitorRedisKeys();
         return;
      } 
      /* -- */
      let  [dbid, tag] = _omms.liveView.client_tag.split("|");
      dbid = dbid.replace("dbid:", "");
      tag = tag.replace("tag:", "");
      /* -- */
      let url = `/api/get/client_circuits?clttag=${tag}`;
      $.get(url, function(jsarr) {
         _omms.liveView.clinet_circuits = [];
            jsarr.forEach((i) => {
                  let cc = new ClientCircuit(i);
                  _omms.liveView.clinet_circuits.push(cc);
               }); 
            console.log(_omms.liveView.clinet_circuits);
            _omms.liveView.monitorRedisKeys();
         });
      /* -- */
   },

   monitorRedisKeys() {
      if (_omms.liveView.client_tag == "") {
         /* stop ticker */  
      } else {
         _omms.liveView.getRedisData();
      }

   },

   getRedisData() {
      let update_utcnow = (jsobj) => {
            $.get("/api/get/utcnow_time", function(resp) {
                  _omms.liveView.server_utcnow = resp.utcnow_time;
                  _this.processKWhrs(jsobj);
               });
         };
      /* make remove call */
      let out = [];
      _omms.liveView.clinet_circuits.forEach((item) => {
            out.push(item.syspath);
         });
      /* -- */    
      let _this = this, 
         sp = out.join("|"), 
         url = `/api/get/redis_data?dbidx=2&keys=[${sp}]`; 
      $.get(url, function(jsobj) {
            update_utcnow(jsobj);     
         });
      /* -- */
   },

   processKWhrs(jsobj) {
      let html = `<div id="vpBodyHdr" class="vp-bdy-hdr"></div>` + 
         `<div id="vpBody" class="view-port-body" />`;
      $("#appViewport").html(html);
      for (let key in jsobj) {
         let _jsobj = jsobj[key];
         this.displayKWhrs(key, _jsobj);
      }
   },

   reading2Dict(buff) {
      if (!(buff[0] == "[" && buff.substr(-1) == "]"))
         throw "BadReadingBuffer";
      buff = buff.replace("[", "").replace("]", "");
      let d = {};
      buff.split("|").forEach(function(e) {
            let [k, v] = e.split(":");
            d[k.trim()] = v.trim();
         });
      return d;
   },

   displayKWhrs(syspath, jsobj) {
      /* -- */
      let find_cirtag = (sp) => {
            return _omms.liveView.clinet_circuits.find(i => i.syspath == sp);
         };
      /* -- */
      let rkey = "#RPT_kWhrs", rval = "";
      if (!(rkey in jsobj))
         throw `KeyNotFound: ${rkey}`;
      rval = jsobj[rkey];
      /* -- */
      let tkey = "#RPT_kWhrs_dtsutc_epoch", tval = "";
      if (!(tkey in jsobj))
         throw `KeyNotFound: ${tkey}`; 
      tval = jsobj[tkey];
      /* -- */
      let data = this.reading2Dict(rval);
      if (data["#RPT"] != "kWhrs")
         throw "BadReport";
      let tkhs = data["tl_kwh"];
      if (tkhs == undefined)
         tkhs = data["kWh"];
      /* -- */
      let [dts, epoch] = tval.split("|");
      dts = dts.trim();
      epoch = parseInt(epoch.trim());
      let diff_m = Math.round((_omms.liveView.server_utcnow - epoch) / 60);
      let bcls = "";
      if (diff_m <= 30) {
         bcls = "color:darkgreen;";
      } else if (diff_m >= 31 && diff_m <= 120) {
         bcls = "color:rgb(145, 96, 6);";
      } else {
         bcls = "color:rgb(179, 8, 8);";
      }
      /* -- */
      let ctag = find_cirtag(syspath).cirtag, 
         cg = `<b0>Circuit:&nbsp;${ctag}</b0>`,
         kwhs = `<b1>Total&nbsp;kWhrs:&nbsp;${tkhs}</b1>`,  
         dtsutc = `<b style="${bcls}">DTS_UTC:&nbsp;${dts}</b>`,
         sp = `SYSPATH:&nbsp;${syspath}`,
         html = `<div class="kwhrs-view">` + 
            `<div class="kwhrs-cg">${cg}&nbsp;|&nbsp;${kwhs}&nbsp;|` +
               `&nbsp;${dtsutc}&nbsp;<small><i>&nbsp;[${diff_m}m]</i></small></div>` + 
            `<div class="msyspath">${sp}</div>` + 
            `<div class="kwhrs-reading">READING:&nbsp;${rval}</div></div>`;
      /* -- -- -- -- */
      $("#vpBodyHdr").html(`last refresh: ${new Date().toLocaleString("pl")}`);
      $("#vpBody").append(html);
   }

};
