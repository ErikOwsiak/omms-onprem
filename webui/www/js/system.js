
var system = {

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

class DateParser {

   constructor() {

   }

   


};
