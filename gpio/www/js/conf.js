
class gpioConf {

   static urlpfx = "/omms/gpio";
   static ctJSON = "application/json";
   static forceUrl = `${gpioConf.urlpfx}/force`;
   static setconfUrl = `${gpioConf.urlpfx}/setconf`;

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
            let _idtag = this.attributes["_idtag"].value,
               dayparts = ["sunrise", "sunset"];
            /* -- */
            let sellMM = document.getElementById(`selMM_${_idtag}`);
            if (dayparts.includes(this.value))
               sellMM.innerHTML =  HTML.selTimeMM(-45, 45, 15);
            else
               sellMM.innerHTML =  HTML.selTimeMM(0, 45, 15);
         };
      /* -- divSel_TimeOn_HH, divSel_TimeOn_MM */
      let div_val = function() {
            let selHv, selMv, 
               _idtag = this.attributes["_idtag"].value,
               selH = document.getElementById(`selHH_${_idtag}`),
               selM = document.getElementById(`selMM_${_idtag}`);
            console.log(`div_val: ${_idtag}`);
            /* -- */
            if (selH != undefined)
               selHv = selH.value;
            if (selM != undefined)
               selMv = selM.value;
            /* -- */
            return [selHv, selMv];
         };
      /* add val calls on the div holding HH & MM selects */
      let divTimeOn = document.getElementById("divSel_TimeOn"),
         divTimeOff = document.getElementById("divSel_TimeOff");
      divTimeOn.val = div_val;
      divTimeOff.val = div_val;
      /* -- select ON hour | onHH */
      let selHHon = document.getElementById("selHH_TimeOn");
      selHHon.innerHTML =  HTML.selTimeHH();
      selHHon.addEventListener("change", hr_sel_chng);
      /* -- select ON minutes | onMM */
      let selMMon = document.getElementById("selMM_TimeOn");
      selMMon.innerHTML =  HTML.selTimeMM(0, 45, 15);
      /* -- select OFF hour | offHH */
      let selHHoff = document.getElementById("selHH_TimeOff");
      selHHoff.innerHTML =  HTML.selTimeHH();
      selHHoff.addEventListener("change", hr_sel_chng);
      /* -- select OFF minutes | offMM */
      let selMMoff = document.getElementById("selMM_TimeOff");
      selMMoff.innerHTML =  HTML.selTimeMM(0, 45, 15);
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
            t.forceOnOff(t.devid, t.chnl, "n/s");
         });
      /* save config info */
      this.btnSave = this.doc.byID("btnSave");
      let btnSaveClick = function() {
            /* -- greb HH selector -- */
            debugger
            let [onHH, onMM] = divTimeOn.val();
            let [offHH, offMM] = divTimeOff.val();
            let chnlName = document.getElementById("txtChnlName").value;
            /* -- */
            sunOn = sunOn.options[sunOn.selectedIndex].value;
            if (tON == ":" && sunOn == "0") {
               alert("Select ON Time!");
               return;
            }
            /* -- */
            sunOff = sunOff.options[sunOff.selectedIndex].value;
            if (tOFF == ":" && sunOff == "0") {
               alert("Select OFF Time!");
               return;
            }
            /* -- */
            sunOnOffset = sunOnOffset.options[sunOnOffset.selectedIndex].value;
            sunOffOffset = sunOffOffset.options[sunOffOffset.selectedIndex].value;
            /* -- */
            let data = {"devid": t.devid, "chnl": t.chnl, tON, tOFF
               , sunOn, sunOff, sunOnOffset, sunOffOffset, chnlName};
            /* -- */
            t.setConf(data);
         };
      /* -- */
      this.btnSave.addEventListener("click", btnSaveClick);
      /* -- */
   }

   onGotConf(d) {
      /* -- */
      gpioConf.onMobile();
      /* -- */
      if (d["CHANNEL_NAME"]) {
         let chnlName = document.getElementById("txtChnlName");
         chnlName.value = (d.CHANNEL_NAME) ? d.CHANNEL_NAME : "";
      }
      if (d["CONF"]) {
         let jobj = JSON.parse(d.CONF);
         /* -- */
         let tON = document.getElementById("timeOn");
         tON.value = jobj.tON;
         let sunOn = document.getElementById("sunSelOn");
         sunOn.value = jobj.sunOn;
         let sunOnOffset = document.getElementById("sunSelOnOffset");
         sunOnOffset.value = jobj.sunOnOffset;
         /* -- */
         let tOFF = document.getElementById("timeOff");
         tOFF.value = jobj.tOFF;
         let sunOff = document.getElementById("sunSelOff");
         sunOff.value = jobj.sunOff;
         let sunOffOffset = document.getElementById("sunSelOffOffset");
         sunOffOffset.value = jobj.sunOffOffset;
      }
      /* -- */
      console.log(d);
      if (d["OVERRIDE"]) {
         const on_css = "4px solid green";
         const off_css = "1px solid darkgrey";
         const override = JSON.parse(d.OVERRIDE);
         let bOn = document.getElementById("btnOverrideON");
         bOn.style.border = off_css;
         let bOff = document.getElementById("btnOverrideOFF");
         bOff.style.border = off_css;
         /* -- */
         switch (override.state) {
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
            alert(jsobj.MSG);
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
            alert(jsobj.MSG);
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
