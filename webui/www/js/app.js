

/* main app class -> entry point */
var app = {

   ZERO_PAD: "0",
   helpUrl: "https://omms.iotech.systems",
   lastClickedMeter: null,
   streamTbl: "",
   realtimeMon: null,
   orgNav: null,
   histogram: null,
   blockedMeterBtns: null,
   /* hold report results */
   lastReports: {clientSpaces: null
      , clientMeters: null},

   /* - - */
   init() {
      clickRouter.init();
      gui.loadDataBlockXml("orgNav", "subMenuCol");
      gui.loadDataBlockXml("systemOverview", "appViewport")
      setTimeout(app.readOmmsUser, 200);
      app.setAcl();
      app.applyAcl();
   },

   setAcl() {
      /* omms_acl=15 */
      let rx = /omms_acl=([0-9]{1,2})/gm;
      let m = rx.exec(document.cookie)
      if (!m)
         return;
      /* -- */
      if (m.length == 2) {
         app.ommsAcl = parseInt(m[1]);
      } else {
         app.ommsAcl = 1;
      }
      /* -- */
   },

   applyAcl() {
      $("appbtn").each((_, appbtn) => {
            let acl = $(appbtn).attr("acl");
            if (app.ommsAcl < acl) {
               $(appbtn).removeClass("hover");
               $(appbtn).css("opacity", "0.28");
               $(appbtn).attr("title", "disabled for your ACL");
               $(appbtn).off();
            }
         });
   },

   /* - - */
   processMeters(jobj) {
      let navTree = new orgXmlNavTree(jobj);
      navTree.loadView("edge_name");
   },

   readOmmsUser() {
      let qkv = new queryStringKeyVal("UID");
      $("#userID").html(qkv.value(null));
   },

   /* http://85.222.109.238:4080/api/get/lastreading/kwhrs/1001 */
   meterOnClick() {
      try {
         /* set last clicked meter */
         app.lastClickedMeter = this;
         /* load gui stuff */
         if ($("#appViewport #streamFrame").length == 0)
            gui.loadDataBlockXml("streamFrame", null);
         /* start running */
         realtimeMonitor.meterDBID = $(this).attr("dbid");
         /* run tick */
         realtimeMonitor.tick();
      } catch(e) {
         system.handleException(e);
         gui.clearViewport();
         gui.loadDataBlockXml("streamFrame", null);   
      }
   },

   blockOutButtons() {
      /* - - */
      let dbid = $(app.lastClickedMeter).attr("dbid"), 
         ctag = $(app.lastClickedMeter).attr("ctag"),
         selector = `div[dbid="${dbid}"].meter_button`;
      /* - - */
      let msg = `loading data for: ${ctag}`;
      $("#orgNavBodyBusy div").html(msg);
      app.fadeOutFadeIn("#orgNavBody", "#orgNavBodyBusy", 280);
      let btn = document.querySelector(selector);
      let ofLeft = btn.parentElement.offsetLeft,
         ofTop = btn.parentElement.offsetTop,
         cltHeight = btn.parentElement.clientHeight,
         cltWidth = btn.parentElement.clientWidth;
   },

   unblockoutButtons() {
      $("#orgNavBodyBusy div").html("");
      app.fadeOutFadeIn("#orgNavBodyBusy", "#orgNavBody", 280);
   },

   showDataLoading(txt) {
      let msg = `loading data for: <b>${txt}</b>`;
      $("#orgNavBodyBusy div").html(msg);
      $("#orgNavBody").fadeOut(280, () => {
            $("#orgNavBodyBusy").fadeIn(280);
         });
   },

   hideDataLoading() {
      $("#orgNavBodyBusy").fadeOut(280, () => {
            $("#orgNavBody").fadeIn(280);
         });
   },

   fadeOutFadeIn(outSelector, inSelector, speed) {
      $(outSelector).fadeOut(speed, () => {
            $(inSelector).fadeIn(speed);
         });
   },

   loadOrgNav() {
      app.orgNav = new orgNavigator();
      app.orgNav.init();
   },

   quickSelectChanged() {
      /* - - */
      let currentDate = new Date();
      let firstDayStr = "",
         lastDayStr = "",
         currentDayOfMonth = currentDate.getDate(),
         currentMonth = currentDate.getMonth(),
         currentFullYear = currentDate.getFullYear(),
         val = $(this).val(),
         selector = "#appViewport #startDate, #appViewport #endDate";
      let dayStr = (currentDayOfMonth < 10) ? `0${currentDayOfMonth}` : `${currentDayOfMonth}`;
      $("#kWhrsRptFrame .kwhrs-rpt-body").html("");
      /* - - */
      switch(val) {
         case "manual":
            {
               $(selector).val("");
               $(selector).removeAttr("disabled");
               return;
            }
         case "today":
            {
               currentMonth++;
               let monthStr = `${currentMonth}`.padStart(2, app.ZERO_PAD); 
               firstDayStr = `${currentFullYear}-${monthStr}-${dayStr}`;
               lastDayStr = firstDayStr;
            }
            break;
         case "thisMonth":
            {
               currentMonth++;
               firstDayStr = app.firstDayDateOfYearMonth(currentFullYear, currentMonth);
               lastDayStr = app.lastDayDateOfYearMonth(currentFullYear, currentMonth);
            }
            break;
         case "lastMonth":
            {
               let arr = app.lastMonth();
               firstDayStr = arr[0];
               lastDayStr = arr[1]; 
            }
            break;
         case "meterTotal":
            {
               currentMonth++;
               firstDayStr = "2020-01-01";
               lastDayStr = app.lastDayDateOfYearMonth(currentFullYear, currentMonth);
            }
            break;
         default:
            break;
      }
      /* - - */
      $("#appViewport #startDate").val(firstDayStr);
      $("#appViewport #endDate").val(lastDayStr);
      $(selector).attr("disabled", "1");
   },

   initStreamFrame() {
      realtimeMonitor.clearTimers();
      realtimeMonitor.streamTbl = null;
      realtimeMonitor.meterDBID = null;
      realtimeMonitor.callback = gui.displayRealtime;
      setTimeout(realtimeMonitor.tick, 200);
   },

   lastMonth() {
      /* -- */
      let [year, month] = app.nowYearMonth();
      /* is jan */
      if (month == 0) {
         year--;
         month = 12;      
      }
      /* - - */
      let fstDay = app.firstDayDateOfYearMonth(year, month),
         lstDay = app.lastDayDateOfYearMonth(year, month);
      /* return */
      return [fstDay, lstDay];
   },

   lastDayDateOfYearMonth(year, month) {
      let d = new Date(year, month, 0), dd = d.getDate(),
         mstr = `${month}`.padStart(2, app.ZERO_PAD),
         dstr = `${dd}`.padStart(2, app.ZERO_PAD);
      /* return string date */
      return `${year}-${mstr}-${dstr}`;
   },

   firstDayDateOfYearMonth(year, month) {
      let  ystr = `${year}`.padStart(2, app.ZERO_PAD),
         mstr = `${month}`.padStart(2, app.ZERO_PAD);
      /* return string date */
      return `${ystr}-${mstr}-01`;
   },

   nowYearMonth() {
      let d = new Date();
      return [d.getFullYear(), d.getMonth()];
   },

   lastFiveYears(selID) {
      let d = new Date();
      for (let i = 0; i < 6; i++) {
         let y = (d.getFullYear() - i);
         $(`#${selID}`).append(`<option value="${y}">${y}</option>`);
      }
   },

   renderReportFiles(jsdata) {
      /* -- */
      let hdr = "kWhrs Monthly Reports";
      $("#kwhrsRptBody").html(`<div class="rpt_lst_hdr">${hdr}</div>`);
      let onyear = function(y, arr) {
            let hdr = `<div class="yr_hdr">${y}</div>`,
               fls = `<div id="YR_${y}" class="year_files"></div>`;
            $("#kwhrsRptBody").append(`${hdr}${fls}`);
            onfiles(y, arr);
            /* add onclick */
            $("div.gd_xl").off().on("click", app.onXmlFileClick);
         };
      /* -- */
      let onfiles = function(y, arr) {
            for (let i = 1; i <= 12; i++) {
               let stri = `${i}`.padStart(2, 0),
                  patt = `_${y}_${stri}.xlsx`, 
                  ln = arr.find(i => i.endsWith(patt));
               /* -- */
               if (ln) {
                  let p = `/reports/${y}/${ln}`, 
                     d = `${y}_${stri}`,  
                     m = `<div xls="${p}" class="gd_xl"><div></div><div>${d}</div></div>`;
                  $(`#YR_${y}`).append(m);
               } else {
                  let m = 
                     `<div class="no_xl"><div></div>NoFile<div></div></div>`;
                  $(`#YR_${y}`).append(m);
               }
            }
         };
      /* -- */
      for (let y in jsdata)
         onyear(y, jsdata[y]);
      /* -- */
   },

   onXmlFileClick() {
      let xls = this.getAttribute("xls");
      console.log(xls);
      window.open(xls, "_blank");
   }

};

/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */
/* attach page loaded event */
window.addEventListener("DOMContentLoaded", app.init);
