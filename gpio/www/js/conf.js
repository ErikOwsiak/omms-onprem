
class gpioConf {

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
      // this.btnOn = document.getElementById("btnOverrideON");
      this.btnOn = this.doc.byID("btnOverrideON");
      this.btnOn.addEventListener("click", this.forceOn);
      /* force off button */
      // this.btnOff = document.getElementById("btnOverrideOFF");
      this.btnOff = this.elmByID("btnOverrideOFF");
      this.btnOff.addEventListener("click", this.forceOff);
      /* save config info */
      this.btnSave = document.getElementById("btnSave");
      this.btnSave.addEventListener("click", this.saveConf);
   }

   forceOn() {
      console.log("fon");
   }

   forceOff() {
      console.log("off");
   }

   saveConf() {
      console.log("save");
   }

};
