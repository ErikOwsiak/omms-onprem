

class wanAccess {

   constructor() {

   }

   init() {
      /* -- */
      this.ctls = `<input type="text" id="waNums" value="" placeholder="enter number hours/days"/>` + 
         `<select id="waNumTypes"><option value="h">hours</option><option value="d">days</option></select>`
         `<input id="bntCreateAccessQRC" type="button" value="CreateAccessQRC" />`;
      /* -- */
      this.frame = `<div class="wa-frame"><div class="wa-qac"></div>` +
         `<div id="waCtrls" class="wa-ctls">${this.ctls}</div></div>`;
      /* -- */
      $("#subMenuCol").html(this.frame);
   }

};
