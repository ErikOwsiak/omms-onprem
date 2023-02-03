
_omms.xmlsecs = {

   LOADED_XML: null,

   settings() {
      /* -- */
      _omms.gui.clearViewport();
      _omms.app.subNav = new submenuNav("settingsMenuBody");
      _omms.app.dataOps = new dataOps();
      /* -- */
      if (_omms.dbedit == null)
         _omms.dbedit = new dbEdit();
      /* -- init -- */
      _omms.dbedit.init();
   },

   clientView() {
      _omms.gui.clearViewport();
      _omms.liveView.init();
      $("#btnRunCltView").off().on("click", _omms.app.onViewCltMeterData);
      $("#selCltSelector").off().on("change", _omms.liveView.onClientSelected);
   },

   cltCirHistory() {
      let callback = function(jsarr) {
            $("#cltCirHistory").html("");
            jsarr.forEach(e => {
                  cch = new CltCirHistory(e);
                  $("#cltCirHistory").append(cch.toHtmlStr());
               });
         };
      let restapi = new restAPI();
      restapi.getClientCircuitHistory(callback);
   }

};
