

class wanAccess {

   constructor() {

   }

   init() {
      /* -- */
      this.ctls = `<input type="text" id="waNums" value="" placeholder="enter number hours/days"/>` + 
         `<select id="waNumTypes"><option value="h">hours</option><option value="d">days</option></select>` +
         `<input id="bntCreateAccessQRC" type="button" value="CreateQRC" />`;
      /* -- */
      this.frame = `<div class="wa-frame"><div class="wa-qac"></div>` +
         `<div id="waCtrls" class="wa-ctls">${this.ctls}</div></div>`;
      /* -- */
      $("#subMenuCol").html(this.frame);
      $("#bntCreateAccessQRC").off().on("click", this.createQRC);
      /* -- */
   }

   createQRC() {
      /* -- */
      let h = $("#waNums").val(), ht = $("#waNumTypes").val();
      /* -- */
      let url = `/omms/ui/api/get/qrc/${h}/${ht}`;
      $.get(url, function(jsobj) {
            console.log(jsobj);
         });
      /* -- */
   }

};
