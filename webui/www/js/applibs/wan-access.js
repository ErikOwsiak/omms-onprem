


class wanAccess {

   constructor() {

   }

   init() {
      alert("xxxxx");
      this.frame = `<div class="wa-frame"><div class="wa-qac"></div>` +
         `<div id="waCtrls" class="wa-ctls"></div></div>`;
      $("#subMenuCol").html(this.frame);
   }

};
