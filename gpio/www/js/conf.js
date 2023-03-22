
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
   }

   forceOnOff(devid, chnl, state) {
      let data = {devid, chnl, state};
      fetch(gpioConf.forceUrl, {method: "POST"
            , headers: {"Content-Type": gpioConf.ctJSON}
            , body: JSON.stringify(data)
         }).then((rsp) => rsp.text()).then((d) => console.log(d));
   }

   setConf(data) {
      fetch(gpioConf.setconfUrl, {method: "POST"
            , headers: {"Content-Type": gpioConf.ctJSON}
            , body: JSON.stringify(data)
         }).then((rsp) => rsp.text()).then((d) => console.log(d));
   }

};
