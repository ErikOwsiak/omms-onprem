
class gpioConf {

   constructor() {
      this.btnOn = null;
      this.btnOff = null;
      this.btnSave = null;
   }

   init() {
      this.btnOn = document.getElementById("btnOverrideON");
      this.btnOn.addEventListener("click", this.forceOn);
      this.btnOff = document.getElementById("btnOverrideOFF");
      this.btnOff.addEventListener("click", this.forceOff);
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
