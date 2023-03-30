

class wanAccess {

   static cntdown = 0;
   static cnttmer = null;

   constructor() {
      this.ctls = null;
      this.frame = null;
   }

   init() {
      /* -- */
      this.ctls = `<input type="text" id="waNums" value="" placeholder="enter number hours/days"/>` + 
         `<select id="waNumTypes"><option value="h">hours</option><option value="d">days</option></select>` +
         `<input id="bntCreateAccessQRC" type="button" value="CreateQRC" />`;
      /* -- */
      this.frame = `<div class="wa-frame"><div id="waQAC" class="wa-qac"></div>` +
         `<div id="waData"></div>` + 
         `<div id="waCtrls" class="wa-ctls">${this.ctls}</div></div>`;
      /* -- */
      $("#subMenuCol").html(this.frame);
      let _this = this;
      $("#bntCreateAccessQRC").off().on("click", function() { 
            _this.createQRC();
         });
      /* -- */
      this.clearQRCTimeout();
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
               /* -- */
               let src = `/omms/ui/imgs/qrc.png?qr=${jsobj.UUID}`, 
                  img = `<img class="qr-img" src="${src}" />`;
               /* -- */
               $("#waQAC").html(`${img}<div id="waCntDown"></div>`);
               $("#waData").text(jsobj.DATA);
               /* -- */
               wanAccess.cntdown = 60;
               clearInterval(wanAccess.cnttmer);
               wanAccess.cnttmer = setInterval(() => {
                     $("#waCntDown").text(wanAccess.cntdown);
                     if (wanAccess.cntdown == 0) {
                        clearInterval(wanAccess.cnttmer);
                        this.clearQRCTimeout();
                     }
                     wanAccess.cntdown--;
                  }, 1000);
               /* -- */
            }
            break;
         default:
            alert(`BadErrorCode: ${jsobj.ERROR}`);
      }
      /* -- */
   }

   clearQRCTimeout() {
      $("#waQAC").html("");
      let txt = "Access QRCode Generator";
      $("#waQAC").html(txt);
   }

};
