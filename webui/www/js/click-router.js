
/* 
   attaches to all the appbtn elemetns 
*/

var clickRouter = {

   rtStreamInputClicks: null,

   init() {
      $("appbtn").on("click", this.click);
      this.rtStreamInputClicks = new appClicks();
      let selector = "#realtimeStreamSelector input"; 
      $(selector).off().on("click", 
         this.rtStreamInputClicks.realtimeStreamOnClick);
   },

   initGraphSelector() {
      let selector = "#realtimeStreamSelector input"; 
      $(selector).off().on("click", 
         this.rtStreamInputClicks.realtimeStreamOnClick);
      $("#histoHrs").off().on("change", () => {
            $(app.lastClickedMeter).click();
         });
   },

   click() {
      try {
         let clickName = `${this.id}Click`;
         clickRouter.onBtnClickToggleCSS(this);
         let appClicksObj = new appClicks();
         appClicksObj[clickName](this);
      } catch(e) {
         console.log(e);
      }
   },

   onBtnClickToggleCSS(__this__) {
      let oneach = (item, arr) => {
            console.log(item, arr);
         };
      /* - - */
      $("appbtn").each(oneach);
   }

}
