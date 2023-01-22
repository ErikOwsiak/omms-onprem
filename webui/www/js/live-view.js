
_omms.liveView = {

   restapi: null,

   init() {
      _omms.liveView.restapi = new restAPI();
      _omms.liveView.restapi.getClients(_omms.liveView.onGetClients);
   },

   run() {
   },

   onGetClients(jsarr) {
      //console.log(jsarr);
      let selector = "#selCltSelector"
      $(selector).html("");
      /* for each clt */
      jsarr.forEach((v, _x, _y) => {
            let [dbid, tag, cltname] = v;
            console.log([dbid, tag, cltname]);
            let val = `dbid:${dbid}|tag:${tag}`;
            $(selector).append(`<option value="${val}">${cltname}</option>`);
         });
      /* -- */
   }

};
