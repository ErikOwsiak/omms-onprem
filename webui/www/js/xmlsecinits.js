
_omms.xmlsecs = {

   settings() {
      _omms.gui.clearViewport();
      _omms.app.subNav = new submenuNav("settingsMenuBody");
      _omms.app.dataOps = new dataOps();
      //_omms.app.dataOps.getOrg();
      if (_omms.dbedit == null)
         _omms.dbedit = new dbEdit();
      /* -- init -- */
      _omms.dbedit.init();
   },

   clientView() {
      _omms.gui.clearViewport();
      _omms.liveView.init();
      $("#btnRunCltView").off().on("click", _omms.app.onViewCltMeterData);
   }
   
};
