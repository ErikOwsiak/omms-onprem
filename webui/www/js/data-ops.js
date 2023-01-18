
class dataOps {

   /*
      static block
   */
   
   static kWhrsReportTotal(jarr) {
      /* - - */
      let t = 0.0, kwhIndex = 5;
      for (let i in jarr) {
         let v = jarr[i][kwhIndex];
         if (v == undefined)
            continue;
         t += parseFloat(v);
      }
      /* - - */
      return parseFloat(t.toFixed(2)).toLocaleString();
   }


   constructor() {
      this.api = new restAPI();
      this.org = null;
   }

   getMetersByType(meterType) { }   

   getLastMeterReading(meterDBID) { }

   getOrg() {
      let __this = this;
      this.api.getOrg((res) => {
            __this.org = res;
         });
   }

   filterOrgOnType(entype) {
      return this.org.filter((o) => o.entity_type == entype);
   }

   getPerClientSpaceSummary(_clt, jarr) {
      /* - - */
      let out = {report: "client_space"
         , clt: _clt, counter: 0, lnsArr: [], lnsObj: {}};
      /* - - */
      jarr.forEach((item) => {
            let tmpObj = null, spaceTag = item[4];
            if (!out.lnsObj[spaceTag]) {
               tmpObj = {"space": spaceTag, "ctags": item[1], "kwhs": item[5], "clt": _clt};
               out.lnsObj[spaceTag] = tmpObj;
               out.counter++;
            } else {
               out.lnsObj[spaceTag].ctags += `, ${item[1]}`;
               out.lnsObj[spaceTag].kwhs += item[5];
            }
         });
      /* - - */
      return out;
   }

   getPerClientMeterSummary(_clt, jarr) {
      /* - - */
      let tmpObj = null 
         , out = {report: "client_meter"
         , clt: _clt, counter: 0, lnsArr: [], lnsObj: {}};
      /* - - */
      jarr.forEach((item) => {
               tmpObj = {"space": item[4], "ctags": item[1], "kwhs": item[5], "clt": _clt};
               out.lnsArr.push(tmpObj);
               out.counter++;
         });
      /* - - */
      return out;
   }

}
