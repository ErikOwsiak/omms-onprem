

class wanAccess {

   constructor() {

   }

   init() {
      /* -- */
      this.ctls = `<input type="text" id="waNums" value="" placeholder="enter number hours/days"/>` + 
         `<select id="waNumTypes"><option value="h">hours</option><option value="d">days</option></select>` +
         `<input id="bntCreateAccessQRC" type="button" value="CreateQRC" />`;
      /* -- */
      this.frame = `<div class="wa-frame"><div id="waQAC" class="wa-qac"></div>` +
         `<div id="waCtrls" class="wa-ctls">${this.ctls}</div>` + 
         `<div id="waData"></div></div>`;
      /* -- */
      $("#subMenuCol").html(this.frame);
      let _this = this;
      $("#bntCreateAccessQRC").off().on("click", function() { 
            _this.createQRC();
         });
      /* -- */
   }

   createQRC() {
      /* -- */
      let h = $("#waNums").val()
         , ht = $("#waNumTypes").val();
      if (h == "" || h === undefined) {
         alert("Enter Time Interval!");
         return;
      }
      /* -- */
      let _this = this
         , url = `/omms/ui/api/get/qrc/${h}/${ht}`;
      $.get(url, function(jsobj) {
            _this.onCreateQRC(jsobj);
         });
      /* -- */
   }

   onCreateQRC(jsobj) {
      /* -- */
      if (jsobj.ERROR == undefined) {
         console.log("BadErrorCode");
         return;
      }
      /* -- */
      switch (jsobj.ERROR) {
         case 0:
            {
               let src = `/omms/ui/imgs/qrc.png?qr=${jsobj.UUID}`, 
                  img = `<img class="qr-img" src="${src}" />`;
               $("#waQAC").html(img);
               $("#waData").text(jsobj.DATA);
            }
            break;
         default:
            alert(`BadErrorCode: ${jsobj.ERROR}`);
      }
      /* -- */
   }

};
