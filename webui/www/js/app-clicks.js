
_omms.__str__ = _omms.strings.en;


class appClicks {

   constructor() {}

   loadOrNavClick() {
      _omms.realtimeMonitor.stop();
      _omms.gui.loadDataBlockXml("orgNav", "subMenuCol");
      _omms.gui.clearViewport();
   }

   systemReportsClick(__this) {
      /* -- */
      _omms.realtimeMonitor.stop();
      _omms.gui.clearViewport();
      /* -- */
      let text = __this.innerText,
         subMsg = _omms.__str__. sysRpts,
         subMenu = _omms.html.subMenuHead(text, subMsg);
      _omms.gui.subMenu.load(subMenu);
      _omms.gui.loadDataBlockXml("xmlReports", "subMenuCol");
      /* -- */
   }

   logoutClick(__this) {
      /* -- */
      _omms.realtimeMonitor.stop();
      _omms.gui.clearViewport();
      /* -- */
      $.get("/omms/ui/logout", (jobj) => {
            if (jobj.error == 0) {
               console.log(document.cookie);
               window.location.href = jobj.nxturl;
            }
         });
      /* -- */
   }

   homeClick() {
      window.location.href = "/omms/ui";
   }

   ogpioClick() {
      try {
         $("#subMenuCol").html("");
         /* -- -- -- -- */
         _omms.app.gpio = new OpenGPIO("appViewport");
         _omms.app.gpio.init();
         /* -- -- -- -- */
         _omms.app.wangate = new wanAccess();
         _omms.app.wangate.init();
      } catch (e) {
         console.log(e);
      }
   }

   liveViewClick() {
      _omms.gui.clearViewport();
      _omms.gui.loadDataBlockXml("xmlClientView", "subMenuCol");
   }

   systemSettingsClick(__this) {
      _omms.realtimeMonitor.stop();
      let text = __this.innerText,
         subMsg = _omms.__str__.sysSettings,
         subMenu = _omms.html.subMenuHead(text, subMsg);
      /* - - */
      _omms.gui.subMenu.load(subMenu);
      _omms.gui.loadDataBlockXml("xmlSettings", "subMenuCol");
   }

   systemHelpClick(__this) {
      _omms.realtimeMonitor.keepTicking = false;
      _omms.gui.loadHelp();
   }

   laodSubmenu(xmlID) {
      let elmt = $(`#${xmlID}`)[0],
         buff = elmt.outerHTML.replace("__script", "<script>");
      buff = buff.replace("script__", "</script>");
      $("#submenuColBody").html(buff);
   }

   realtimeStreamOnClick() {
      _omms.gui.lastHistogramMD5 = null;
      if (_omms.app.lastClickedMeter)
         $(_omms.app.lastClickedMeter).click();
   }

   run_kWhrsReport() {
      /* - - */
      let api = new restAPI(),
         aggreateOn = $("#selAggreateOn").val(),
         startDate = $("#startDate").val(),
         endDate = $("#endDate").val(),
         totalOnly = $("#totalOnly").is(":checked");
      /* - - */
      let badInputs = ["", null, undefined];
      if (badInputs.includes(startDate) || badInputs.includes(endDate)) {
         alert("You must select START and END date!");
         return;
      }
      /* - - */
      _omms.app.kwhrsReport = {"dts": new Date(), "jarrs": []};
      /* clear last report results */
      _omms.app.lastReports["clientSpaces"] = [];
      _omms.app.report_kwh = new kWhrsReport(api, aggreateOn, startDate, endDate, totalOnly);
      _omms.app.report_kwh.run();
      /* - - */
      _omms.app.lightBoxedPane = new lightBoxedPane("", "", "");
      let spinner = `<div id="idSpinner" class="loading-spinner">` + 
         `<div class="spinner-msg">loading...</div></div>`;
         _omms.app.lightBoxedPane.showLoading(spinner);
      /* - - */
   }

   export_kWhrsReport() {
      /* - - */
      let sdate = $("#startDate").val(),
         edate = $("#endDate").val(),
         title0 = "kWh Report Export Preview",
         title1 = `<span class="kwhrs-t1">report dates: ${sdate} :: ${edate}</span>`,
         bottomHtml = _omms.html.kWhPreviewBottomBar(),
         repSelector = $("#selAggreateOn").val(),
         reportHtml = kWhrsReport.getReportHtmlPreview(repSelector); 
      /* - - */
      console.log(repSelector);
      _omms.app.lbPane = new lightBoxedPane(title0, title1, reportHtml);
      _omms.app.lbPane.show();
      _omms.app.lbPane.loadBottomBar(bottomHtml);
      /* btnSave_kWhReport */
      let selector = "input#btnSave_kWhReport";
      $(selector).off().on("click", function() {
            let filename = `kWhReport__${sdate}_${edate}.csv`;
            _omms.app.report_kwh.saveCSV(filename);
         });
   }
}
