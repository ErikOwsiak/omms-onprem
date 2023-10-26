
class gpioConf {

   static urlpfx = "/omms/gpio";
   static ctJSON = "application/json";
   static forceUrl = `${gpioConf.urlpfx}/force`;
   static setconfUrl = `${gpioConf.urlpfx}/setconf`;
   static DAYPARTS = ["sunrise", "sunset"];

   constructor(devid, chnl) {
      this.devid = devid;
      this.chnl = chnl;
      this.btnOn = null;
      this.btnOff = null;
      this.btnSave = null;
      this.doc = document;
      this.doc.byID = this.doc.getElementById;
   }

   init() {
      /* -- */
      let t = this;
      let hr_sel_chng = function() {
            let _idtag = this.attributes["_idtag"].value;
            let sellMM = document.getElementById(`selMM_${_idtag}`);
            if (gpioConf.DAYPARTS.includes(this.value))
               sellMM.innerHTML =  HTML.selTimeMM(-45, 45, 15, "+");
            else
               sellMM.innerHTML =  HTML.selTimeMM(0, 55, 5);
         };
      /* -- divSel_TimeOn_HH, divSel_TimeOn_MM */
      let div_val = function() {
            let selHv, selMv, 
               _idtag = this.attributes["_idtag"].value,
               selH = document.getElementById(`selHH_${_idtag}`),
               selM = document.getElementById(`selMM_${_idtag}`);
            /* -- */
            if (selH != undefined)
               selHv = selH.value;
            if (selM != undefined)
               selMv = selM.value;
            /* -- */
            return [selHv, selMv];
         };
      /* -- setter --
         OFF: "sunrise:-30"
         ON: "sunset:15"
         OFF: "05:30"
         ON: "sunset:-15" */
      let set_val = function(val, idtag) {
            console.log(val);
            let [hh, mm] = val.split(":");
            let divHH = document.getElementById(`selHH_${idtag}`),
               divMM = document.getElementById(`selMM_${idtag}`);
            /* -- */
            divHH.value = hh;
            if (gpioConf.DAYPARTS.includes(hh)) {
               divMM.innerHTML = HTML.selTimeMM(-45, 45, 15, "+");
               divMM.value = mm;
            } else {
               divMM.innerHTML = HTML.selTimeMM(0, 55, 5);
               divMM.value = mm;
            }            
         };
      /* add val calls on the div holding HH & MM selects */
      let divTimeOn = document.getElementById("divSel_TimeOn"),
         divTimeOff = document.getElementById("divSel_TimeOff");
      /* -- */
      divTimeOn.val = div_val; 
      divTimeOn.setval = set_val;
      divTimeOff.val = div_val;
      divTimeOff.setval = set_val;
      /* -- select ON hour | onHH */
      let selHHon = document.getElementById("selHH_TimeOn");
      selHHon.innerHTML =  HTML.selTimeHH();
      selHHon.addEventListener("change", hr_sel_chng);
      /* -- select ON minutes | onMM */
      let selMMon = document.getElementById("selMM_TimeOn");
      selMMon.innerHTML =  HTML.selTimeMM(0, 55, 5);
      console.log(selHHon.innerHTML);
      /* -- select OFF hour | offHH */
      let selHHoff = document.getElementById("selHH_TimeOff");
      selHHoff.innerHTML =  HTML.selTimeHH();
      selHHoff.addEventListener("change", hr_sel_chng);
      /* -- select OFF minutes | offMM */
      let selMMoff = document.getElementById("selMM_TimeOff");
      selMMoff.innerHTML =  HTML.selTimeMM(0, 55, 5);
      console.log(selMMoff.innerHTML);
      /* force on button */
      this.btnOn = this.doc.byID("btnOverrideON");
      this.btnOn.addEventListener("click", function() {
            t.forceOnOff(t.devid, t.chnl, "on");
         });
      /* force off button */
      this.btnOff = this.doc.byID("btnOverrideOFF");
      this.btnOff.addEventListener("click", function() {
            t.forceOnOff(t.devid, t.chnl, "off");
         });
      /* force clear */
      this.btnClr = this.doc.byID("btnOverrideCLR");
      this.btnClr.addEventListener("click", function() {
            t.forceOnOff(t.devid, t.chnl, "NIL");
         });
      /* save config info */
      this.btnSave = this.doc.byID("btnSave");
      let btnSaveClick = function() {
            /* -- greb HH selector -- */
            let [onHH, onMM] = divTimeOn.val();
            let [offHH, offMM] = divTimeOff.val();
            let chnlName = document.getElementById("txtChnlName").value;
            /* -- */
            let data = {"devid": t.devid, "chnl": t.chnl, chnlName
               , "ON": `${onHH}:${onMM}`, "OFF": `${offHH}:${offMM}`
               , "HOLIDAY_ON": "00:00", "HOLIDAY_OFF": "00:00"};
            /* -- */
            t.setConf(data);
         };
      /* -- */
      this.btnSave.addEventListener("click", btnSaveClick);
      this.pullState(this);
      /* -- */
   }

   onGotConf(d) {
      /* -- */
      gpioConf.onMobile();
      let divTimeOn = document.getElementById("divSel_TimeOn"),
         divTimeOff = document.getElementById("divSel_TimeOff");
      /* -- */
      if (d["CHANNEL_NAME"]) {
         let chnlName = document.getElementById("txtChnlName");
         chnlName.value = (d.CHANNEL_NAME) ? d.CHANNEL_NAME : "";
      }
      /* -- */
      if (d["ON"])
         divTimeOn.setval(d.ON, "TimeOn");
      /* -- */
      if (d["OFF"])
         divTimeOff.setval(d.OFF, "TimeOff");
      /* -- */
      if (d["OVERRIDE"]) {
         const on_css = "4px solid green";
         const off_css = "1px solid darkgrey";
         let bOn = document.getElementById("btnOverrideON");
         bOn.style.border = off_css;
         let bOff = document.getElementById("btnOverrideOFF");
         bOff.style.border = off_css;
         /* -- */
         switch (d.OVERRIDE) {
            case "on":
                  bOn.style.border = on_css;
               break;
            case "off":
                  bOff.style.border = on_css;
               break;
            default:
               break;
         }
         /* -- */
      }
   }

   forceOnOff(devid, chnl, state) {
      let ondone = function(jsobj) {
            let fb = document.getElementById("feedbackBox");
            fb.innerHTML = jsobj.MSG;
            setTimeout(function() {
                  fb.innerHTML = "";
               }, 2000);
         };
      let data = {devid, chnl, state};
      fetch(gpioConf.forceUrl, {method: "POST"
            , headers: {"Content-Type": gpioConf.ctJSON}
            , body: JSON.stringify(data)
         }).then((rsp) => rsp.json()).then(ondone);
      /* -- */
      let t = this;
      setTimeout(() => {
            t.pullState(t);
         }, 1000);
      /* -- */
   }

   setConf(data) {
      let ondone = function(jsobj) {
            let fb = document.getElementById("feedbackBox");
            fb.innerHTML = jsobj.MSG;
            setTimeout(function() {
                  fb.innerHTML = "";
               }, 2000);
         };
      fetch(gpioConf.setconfUrl, {method: "POST"
            , headers: {"Content-Type": gpioConf.ctJSON}
            , body: JSON.stringify(data)
         }).then((rsp) => rsp.json()).then(ondone);
      /* -- */
      let t = this;
      setTimeout(() => {
            t.pullState(t);
         }, 1000);
      /* -- */
   }

   pullState(t) {
      let url = `/omms/gpio/getconf/${t.devid}/${t.chnl}`;
      fetch(url).then((rsp) => rsp.json()).then(t.onGotConf);
   }

   static onMobile() {
      let mode = document.getElementById("pageMode");
      if (mode.value == "mobile") {
         let e = document.getElementById("txtChnlName");
         e.disabled = "1";
      }
   }

};
