
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
      /* on time */
      let hr_sel_chng = function() {
            let _id = this.attributes["_idtag"].value,
               dayparts = ["sunrise", "sunset"];
            /* -- */
            let div = document.querySelector(`#divSel_${_id}_MM`);
            if (dayparts.includes(this.value)) {
               div.innerHTML =  HTML.selTimeMM(_id, "timeon-css", -45, 45, 15);
            } else {
               div.innerHTML =  HTML.selTimeMM(_id, "timeon-css", 0, 45, 15);
            }
         };
      /* -- */
      let div_val = function() {
            let divHv = document.getElementById(`selHH_${this.id}`).val(),
               divMv = document.getElementById(`selMM_${this.id}`).val();
            return [divHv, divMv];
         };
      /* -- TimeON selector -- */
      let _id = "TimeOn", lbl = "TimeON", sel = `selHH_${_id}`,
         div = document.querySelector(`#divSel_${_id}`);
      div.innerHTML =  HTML.selTimeHH(lbl, _id, "timeon-css");
      div.val = div_val;
      document.getElementById(sel).addEventListener("change", hr_sel_chng);
      div = document.querySelector(`#divSel_${_id}_MM`);
      div.innerHTML =  HTML.selTimeMM(_id, "timeon-css", 0, 45, 15);
      /* off time */
      _id = "TimeOff", lbl = "TimeOFF", sel = `selHH_${_id}`,
         div = document.querySelector(`#divSel_${_id}_HH`);
      div.innerHTML =  HTML.selTimeHH(lbl, _id, "timeon-css");
      div.val = div_val;
      document.getElementById(sel).addEventListener("change", hr_sel_chng);
      div = document.querySelector(`#divSel_${_id}_MM`);
      div.innerHTML =  HTML.selTimeMM(_id, "timeon-css", 0, 45, 15);
      //div = this.doc.byID("divSelTimeOff");
      //div.innerHTML =  HTML.selTime("TimeOFF", "timeOff", "timeon-css");
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
            /* -- */
            let tdiv = document.getElementById("divSel_TimeOn");
            console.log(tdiv.val());
            //console.log([T0, T1]);
            /* -- */
            let tOFF = document.getElementById("divSel_TimeOff").val(),
               sunOff = document.getElementById("sunSelOff"),
               sunOffOffset = document.getElementById("sunSelOffOffset"),
               chnlName = document.getElementById("txtChnlName").value;
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
