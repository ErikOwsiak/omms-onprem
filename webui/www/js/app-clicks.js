
__str__ = strings.en;


class appClicks {

   constructor() {}

   loadOrNavClick() {
      realtimeMonitor.stop();
      gui.loadDataBlockXml("orgNav", "subMenuCol");
      gui.clearViewport();
   }

   systemReportsClick(__this) {
      realtimeMonitor.stop();
      gui.clearViewport();
      /* - - */
      let text = __this.innerText,
         subMsg = __str__. sysRpts,
         subMenu = html.subMenuHead(text, subMsg);
      gui.subMenu.load(subMenu);
      /* - - */
      gui.loadDataBlockXml("xmlReports", "subMenuCol");
   }

   logoutClick(__this) {
      realtimeMonitor.stop();
      gui.clearViewport();
      /* - - */
      $.get("/do/logout", (jobj) => {
            if (jobj.error == 0) {
               console.log(document.cookie);
               window.location.href = jobj.nxturl;
            }
         });
   }

   homeClick() {
      window.location.href = "/home";
   }

   ogpioClick() {
      try {
         app.gpio = new OpenGPIO("appViewport");
         app.gpio.init();
      } catch (e) {
         console.log(e);
      }
   }

   liveViewClick() {
      //realtimeMonitor.stop();
      gui.loadDataBlockXml("liveViewFrame", "subMenuCol");
      gui.clearViewport();   
   }

   systemSettingsClick(__this) {
      realtimeMonitor.stop();
      let text = __this.innerText,
         subMsg = __str__.sysSettings,
         subMenu = html.subMenuHead(text, subMsg);
      /* - - */
      gui.subMenu.load(subMenu);
      gui.loadDataBlockXml("xmlSettings", "subMenuCol");
   }

   systemHelpClick(__this) {
      realtimeMonitor.keepTicking = false;
      gui.loadHelp();
   }

   laodSubmenu(xmlID) {
      let elmt = $(`#${xmlID}`)[0];
      let buff = elmt.outerHTML.replace("__script", "<script>");
      buff = buff.replace("script__", "</script>");
      /* load into the DOM */
      $("#submenuColBody").html(buff);
   }

   realtimeStreamOnClick() {
      gui.lastHistogramMD5 = null;
      if (app.lastClickedMeter)
         $(app.lastClickedMeter).click();
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
      app.kwhrsReport = {"dts": new Date(), "jarrs": []};
      /* clear last report results */
      app.lastReports["clientSpaces"] = [];
      app.report_kwh = new kWhrsReport(api, aggreateOn, startDate, endDate, totalOnly);
      app.report_kwh.run();
      /* - - */
      app.lightBoxedPane = new lightBoxedPane("", "", "");
      let spinner = `<div id="idSpinner" class="loading-spinner">` + 
         `<div class="spinner-msg">loading...</div></div>`;
      app.lightBoxedPane.showLoading(spinner);
      /* - - */
   }

   export_kWhrsReport() {
      /* - - */
      let sdate = $("#startDate").val(),
         edate = $("#endDate").val(),
         title0 = "kWh Report Export Preview",
         title1 = `<span class="kwhrs-t1">report dates: ${sdate} :: ${edate}</span>`,
         bottomHtml = html.kWhPreviewBottomBar(),
         repSelector = $("#selAggreateOn").val(),
         reportHtml = kWhrsReport.getReportHtmlPreview(repSelector); 
      /* - - */
      console.log(repSelector);
      app.lbPane = new lightBoxedPane(title0, title1, reportHtml);
      app.lbPane.show();
      app.lbPane.loadBottomBar(bottomHtml);
      /* btnSave_kWhReport */
      let selector = "input#btnSave_kWhReport";
      $(selector).off().on("click", function() {
            let filename = `kWhReport__${sdate}_${edate}.csv`;
            app.report_kwh.saveCSV(filename);
         });
   }

}
