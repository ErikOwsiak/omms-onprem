
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
      let t = this;
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
      this.btnSave.addEventListener("click", function() {
            let tON = document.getElementById("timeOn").value,
               sunOn = document.getElementById("sunSelOn"),
               sunOnOffset = document.getElementById("sunSelOnOffset"),
               /* -- */
               tOFF = document.getElementById("timeOff").value,
               sunOff = document.getElementById("sunSelOff"),
               sunOffOffset = document.getElementById("sunSelOffOffset"),
               chnlName = document.getElementById("txtChnlName").value;
            /* -- */
            sunOn = sunOn.options[sunOn.selectedIndex].value;
            if (sunOn != "0")
               tON = ""
            sunOff = sunOff.options[sunOff.selectedIndex].value;
            if (sunOff != "0")
               tOFF = ""
            /* -- */
            sunOnOffset = sunOnOffset.options[sunOnOffset.selectedIndex].value;
            sunOffOffset = sunOffOffset.options[sunOffOffset.selectedIndex].value;
            /* -- */
            let data = {"devid": t.devid, "chnl": t.chnl, tON, tOFF
               , sunOn, sunOff, sunOnOffset, sunOffOffset, chnlName};
            /* -- */
            t.setConf(data);
         });
      /* -- */
      t.pullState(t);
   }

   onGotConf(d) {
      /* -- */
      /* -- */
      if (d["CHANNEL_NAME"]) {
         let chnlName = document.getElementById("txtChnlName");
         chnlName.value = (d.CHANNEL_NAME) ? d.CHANNEL_NAME : "";
         let mode = document.getElementById("pageMode");
         if (mode.value == "mobile")
            chnlName.attributes["readonly"] = true;
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
      let data = {devid, chnl, state};
      fetch(gpioConf.forceUrl, {method: "POST"
            , headers: {"Content-Type": gpioConf.ctJSON}
            , body: JSON.stringify(data)
         }).then((rsp) => rsp.text()).then((d) => console.log(d));
      /* -- */
      let t = this;
      setTimeout(() => {
            t.pullState(t);
         }, 1000);
      /* -- */
   }

   setConf(data) {
      fetch(gpioConf.setconfUrl, {method: "POST"
            , headers: {"Content-Type": gpioConf.ctJSON}
            , body: JSON.stringify(data)
         }).then((rsp) => rsp.text()).then((d) => console.log(d));
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
};
