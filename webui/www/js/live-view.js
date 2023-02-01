
_omms.liveView = {

   restapi: null,
   client_tag: null,
   clinet_circuits: null,

   init() {
      _omms.liveView.restapi = new restAPI();
      _omms.liveView.restapi.getClients(_omms.liveView.onGetClients);
   },

   run() {
   },

   onGetClients(jsarr) {
      let selector = "#selCltSelector"
      $(selector).html("");
      /* for each clt */
      let opt = `<option value="" selected>-- select client --</option>`;
      $(selector).append(opt);
      jsarr.forEach((v, _x, _y) => {
            let [dbid, tag, cltname] = v;
            let val = `dbid:${dbid}|tag:${tag}`;
            $(selector).append(`<option value="${val}">${cltname}</option>`);
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
            _this.processKWhrs(jsobj);     
         });
      /* -- */
   },

   processKWhrs(jsobj) {
      $("#appViewport").html(`<div id="vpBody" class="view-port-body" />`);
      for (let key in jsobj) {
         let _jsobj = jsobj[key];
         this.displayKWhrs(key, _jsobj);
      }
   },

   /* const regex = /\|(tl_kwh:\d*\.?\d*)\|/gm;
      // Alternative syntax using RegExp constructor
      // const regex = new RegExp('\\|(tl_kwh:\\d*\\.?\\d*)\\|', 'gm')

      const str = `[ModbusAddr:50|tl_kwh:3068.52|l1_kwh:1619.71|l2_kwh:318.74|l3_kwh:1130.07]`;
      let m;

      while ((m = regex.exec(str)) !== null) {
         // This is necessary to avoid infinite loops with zero-width matches
         if (m.index === regex.lastIndex) {
            regex.lastIndex++;
         }
         
         // The result can be accessed through the `m`-variable.
         m.forEach((match, groupIndex) => {
            console.log(`Found match, group ${groupIndex}: ${match}`);
         });
      } */
   displayKWhrs(syspath, jsobj) {
      /* -- */
      let fix_rval = (val) => {
            const rgx = /\|(tl_kwh:\d*\.?\d*)\|/gm;
            /* get total kwh part */
            let rx = /\|tl_kwh:[0-9]{1,16} \|/;
            val = val.replaceAll("|", "<b>&nbsp;|&nbsp;</b>")
               .replace("tl_kwh:", "<b>TOTAL_kwh:&nbsp;</b>")
               .replace("kWh:", "<b>TOTAL_kwh:&nbsp;</b>");
            val = val.replace("[", "<b>[</b>&nbsp;")
               .replace("]", "<b>&nbsp;]</b>");
            return val;
         };
      /* -- */
      let find_cirtag = (sp) => {
            return _omms.liveView.clinet_circuits.find(i => i.syspath == sp);
         };
      /* -- */
      let rkey = "#RPT_kWhrs", rval = "";
      if (rkey in jsobj)
         rval = fix_rval(jsobj[rkey]);
      /* -- */
      let tkey = "#RPT_kWhrs_dts_utc", tval = "";
      if (tkey in jsobj)
         tval = jsobj[tkey];
      /* -- */
      let ctag = find_cirtag(syspath).cirtag, 
         cg = `Circuit: <b>${ctag}</b>`, 
         sp = `SYSPATH: ${syspath}`, 
         dtsutc = `DTS_UTC: ${tval}`,
         html = `<div class="kwhrs-view"><div class="kwhrs-cg">${cg} | ${sp}</div>` + 
            `<div class="dtsutc">${dtsutc}</div>` + 
            `<div class="kwhrs-reading">READING: ${rval}</div></div>`;
      /* -- -- -- -- */
      $("#vpBody").append(html);   
   }

};
