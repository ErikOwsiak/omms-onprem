
class gpioConf {

   static urlpfx = "/omms/gpio";

   constructor() {
      this.btnOn = null;
      this.btnOff = null;
      this.btnSave = null;
      this.doc = document;
      this.doc.byID = this.doc.getElementById;
      this.elmByID = this.doc.getElementById;
   }

   init() {
      /* force on button */
      this.btnOn = this.doc.byID("btnOverrideON");
      this.btnOn.addEventListener("click", this.forceOn);
      /* force off button */
      this.btnOff = this.doc.byID("btnOverrideOFF");
      this.btnOff.addEventListener("click", this.forceOff);
      /* save config info */
      this.btnSave = this.doc.byID("btnSave");
      this.btnSave.addEventListener("click", this.saveConf);
   }

   forceOn() {
      console.log("fon");
      const devid = "devid";
      const chnl = "chnl";
      const state = "on";
      const url = `${gpioConf.urlpfx}/force/${devid}/${chnl}/${state}`;
      fetch(url).then((rsp) => rsp.text()).then((d) => console.log(d));
   }

   forceOff() {
      console.log("off");
   }

   saveConf() {
      console.log("save");
   }

};
