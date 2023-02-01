
/* global data types */
class ClientCircuit {
   /* select t.row_sid
      , t.locl_tag
      , t.cir_tag
      , m.met_rowid 
      , emc.met_syspath
      , t.code */
   constructor([ccid, locltag, cirtag, metrowid, syspath, code]) {
      this.ccrid = ccid;
      this.locltag = locltag;
      this.cirtag = cirtag;
      this.metrowid = metrowid;
      this.syspath = syspath;
      this.code = code;
   }
}


_omms.system = {

   handleException(e) {
      console.log(e);
      alert(e);
   }

};

class queryStringKeyVal {

   constructor(queryStrKey) {
      this.qsk = queryStrKey; 
   }

   value(defVal = null) {
      let re = new RegExp(`${this.qsk}=([\\w+\\.]{2,32})&{0,1}`, "gm"),
         m = re.exec(window.location.href);
      if ((m == null) || (m.length != 2))
         return defVal;
      /* - - */
      return m[1].trim();
   }

};
