
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
      this.elmByID = this.doc.getElementById;
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
            let d = {"devid": t.devid, "chnl": t.chnl};
            t.setConf(d);
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
