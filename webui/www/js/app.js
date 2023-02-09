
/* main app class -> entry point */
_omms.app = {

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
      _omms.clickRouter.init();
      /* _omms.gui.loadDataBlockXml("orgNav", "subMenuCol");
         _omms.gui.loadDataBlockXml("systemOverview", "appViewport") */
      // setTimeout(_omms.app.readOmmsUser, 200);
      // _omms.app.setAcl();
      // _omms.app.applyAcl();
   },

   setAcl() {
      /* omms_acl=15 */
      let rx = /omms_acl=([0-9]{1,2})/gm;
      let m = rx.exec(document.cookie)
      if (!m)
         return;
      /* -- */
      if (m.length == 2) {
         _omms.app.ommsAcl = parseInt(m[1]);
      } else {
         _omms.app.ommsAcl = 1;
      }
      /* -- */
   },

   applyAcl() {
      $("appbtn").each((_, appbtn) => {
            let acl = $(appbtn).attr("acl");
            if (_omms.app.ommsAcl < acl) {
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
         _omms.app.lastClickedMeter = this;
         /* load gui stuff */
         if ($("#appViewport #streamFrame").length == 0)
            _omms.gui.loadDataBlockXml("streamFrame", null);
         /* start running */
         _omms.realtimeMonitor.meterDBID = $(this).attr("dbid");
         /* run tick */
         _omms.realtimeMonitor.tick();
      } catch(e) {
         _omms.system.handleException(e);
         _omms.gui.clearViewport();
         _omms.gui.loadDataBlockXml("streamFrame", null);   
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
      _omms.app.fadeOutFadeIn("#orgNavBody", "#orgNavBodyBusy", 280);
      let btn = document.querySelector(selector);
      let ofLeft = btn.parentElement.offsetLeft,
         ofTop = btn.parentElement.offsetTop,
         cltHeight = btn.parentElement.clientHeight,
         cltWidth = btn.parentElement.clientWidth;
   },

   unblockoutButtons() {
      $("#orgNavBodyBusy div").html("");
      _omms.app.fadeOutFadeIn("#orgNavBodyBusy", "#orgNavBody", 280);
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
      _omms.app.orgNav = new orgNavigator();
      _omms.app.orgNav.init();
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
      switch (val) {
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
               firstDayStr = _omms.app.firstDayDateOfYearMonth(currentFullYear, currentMonth);
               lastDayStr = _omms.app.lastDayDateOfYearMonth(currentFullYear, currentMonth);
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
               lastDayStr = _omms.app.lastDayDateOfYearMonth(currentFullYear, currentMonth);
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
      _omms.realtimeMonitor.clearTimers();
      _omms.realtimeMonitor.streamTbl = null;
      _omms.realtimeMonitor.meterDBID = null;
      _omms.realtimeMonitor.callback = gui.displayRealtime;
      _omms.setTimeout(realtimeMonitor.tick, 200);
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
            $("div.gd_xl").off().on("click", _omms.app.onXmlFileClick);
         };
      /* -- */
      let onfiles = function(y, arr) {
            for (let i = 1; i <= 12; i++) {
               let mn = `${i}`.padStart(2, 0),
                  patt = `_${y}_${mn}_`, 
                  ln = arr.find(i => i.includes(patt));
               /* -- */
               if (ln) {
                  let p = `/reports/${y}/${ln}`, d = `${y}_${mn}`,
                     m = `<div title="${ln}" xls="${p}" class="gd_xl">` + 
                        `<div></div><div>${d}</div></div>`;
                  $(`#YR_${y}`).append(m);
               } else {
                  let m = `<div class="no_xl"><div></div>NoFile<div></div></div>`;
                  $(`#YR_${y}`).append(m);
               }
            }
         };
      /* -- */
      for (let y in jsdata) {
         if (y != "backup")
            onyear(y, jsdata[y]);
      }
      /* -- */
   },

   onXmlFileClick() {
      let xls = this.getAttribute("xls");
      console.log(xls);
      window.open(xls, "_blank");
   },

   onViewCltMeterData() {
      /* -- */
      let v = $("#selCltSelector").val(),
         d = $("#txtCltViewDate").val();
      if (d == "") {
         alert("Select Date!");
         return;
      }
      let arr = v.split("|");
      if (arr.length != 2) {
         alert("SelectedValueParseError!");
         return;
      }
      /* -- */
      let [dbid, tag] = arr;
      dbid = dbid.replace("dbid:", "").trim();
      tag = tag.replace("tag:", "").trim();
      /* -- */
      let restapi = new restAPI();
      restapi.getClientCircuitsV1(tag, function(jsarr) {
            let lst = [];
            jsarr.forEach(function(i) {
                  lst.push(i[2]);
               });
            /* -- */
            let cirs = lst.join("|"), dts = $("#txtCltViewDate").val();
            if (dts == undefined || dts == "") {
               alert("Select Date");
               return;
            }
            /* -- */
            restapi.getClinetKWhrs(dts, cirs, function(jsarr) {
                  _omms.app.displayClientMeterData(dts, jsarr);
               });
         });
      /* -- */
   },

   displayClientMeterData(dts, jsarr) {
      /* -- */
      let lng = window.navigator.language,
         dt = new Date().toLocaleString(lng), 
         right_div = `<div id="hdrTKWH" class="hdr-tkwh"></div>` +
         `<div id="hdrLastDTS">last refresh: ${dt}</div>`;
      $("#vpBodyHdr").html(right_div);
      $("#vpBody").html("");
      /* -- */
      let tkwh = 0.0;
      jsarr.forEach((i) => {
            let ck = new ClientKWhrs(dts, i);
            $("#vpBody").append(ck.toHtmlStr());
            tkwh += ck.total_kwh;
         });
      /* -- */
      $(`#hdrTKWH`).html(`Total kWh: ${tkwh.toFixed(2)}`);
   },

   startMonthyReport() {
      let y = $("#yearSel").val(),
         m = $("#monthSel").val();
      let url = "/api/post/monthly-report";
      /* -- */
      $.post(url, {"year": y, "month": m}, function(jsobj) {
            let msg = "";
            if (jsobj.REPORT_ID) {
               let rid = parseInt(jsobj.REPORT_ID),
                  d = new Date();
               d.setMinutes(d.getMinutes() + 5);
               let t = d.toLocaleTimeString(); 
               msg = `New Report JobID: ${rid}<br/>For Date: ${y}/${m}<br/>` + 
                  `Click [Show Reports] In:<br/>5 Minutes<br/>around: ${t}`;
            } else {
               msg = "NewRerpotJobError";
            }
            /* -- */
            $("#rptFeedbackDiv").html(msg);
         });
      /* -- */
   }

};


/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */
/* attach page loaded event */
window.addEventListener("DOMContentLoaded", _omms.app.init);
