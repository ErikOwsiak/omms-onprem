
/* global data types */
class ClientCircuit {
   /*select t.row_sid
      , t.locl_tag
      , t.cir_tag 
      , emc.met_syspath
      , t.code */
   constructor([ccid, locltag, cirtag, syspath, code]) {
      this.ccrid = ccid;
      this.locltag = locltag;
      this.cirtag = cirtag;
      this.syspath = syspath;
      this.code = code;
   }
};

class CltCirHistory {
   /*cc.locl_tag
      , cc.cir_tag
      , emc.met_syspath
      , cc.bitflags
      , cast(cc.dt_link as varchar)
      , cast(cc.dt_unlink as varchar)
      , c.clt_name
      , cast(c.dt_crd as varchar)
      , cast(c.dt_del as varchar)*/
   constructor([ltag, ctag, syspath, fbits, dtlnk, dtunlk, cltname, dtcrd, dtdel]) {
      this.ltag = ltag;
      this.ctag = ctag;
      this.syspath = syspath;
      this.fbits = fbits;
      this.dtlnk = dtlnk;
      this.dtunlk = dtunlk;
      this.cltname = cltname;
      this.dtcrd = dtcrd;
      this.dtdel = dtdel;
   }

   toHtmlStr() {
      let ln0 = `<div><b>CLIENT:</b>&nbsp;${this.cltname} | ${this.dtcrd} | ${this.dtdel}</div>`,
         ln1 = `<div><b>CIRCUIT:</b>&nbsp;${this.ltag} | ${this.ctag} | ${this.fbits}` + 
            `| ${this.dtlnk} | ${this.dtunlk}</div>`,
         ln2 = `<div><b>SYSPATH:</b>&nbsp;${this.syspath}</div>`;
      return `<div class="del-item">${ln0}${ln1}${ln2}</div>`;
   }

};

/* 
   select t.met_dbid
   , '{ct}'
   , cast(t.dts_utc::timestamp(0) as varchar)
   , t.total_kwhs
   , t.l1_kwhs
   , t.l2_kwhs
   , t.l3_kwhs 
*/
class ClientKWhrs {

   constructor(dts, arr) {
      this.dts = dts;
      this.arr = arr;
      this.total_kwh = 0.0;
   }

   toHtmlStr() {
      if (this.arr.length == 3) {
         /* -- */
         let [mrowid, cirtag, sp] = this.arr;
         let hdr = `<div class="kwhs-hdr">Search Date ${this.dts}</div>`,
            bdy = `<div>MeterCircuit RowID: ${mrowid} | Circuit: ${cirtag} | NoDataFound</div>`,
            spdiv = `<div class="sp-div">SYSPATH: ${sp}</div>`;
         /* -- */
         return `<div class="kwhs-reading">${hdr}${bdy}${spdiv}</div>`;
      } else if (this.arr.length == 8) {
         /* -- */
         let [mrowid, cirtag, rdts, tkhws, l1khws, l2khws, l3khws, sp] = this.arr;
         let hdr = `<div class="kwhs-hdr">Search Date: <bbl>${this.dts}</bbl></div>`,
            bdy = `<div>MeterCircuit RowID: ${mrowid} | <b>Circuit: ${cirtag}</b> | ReadDTS UTC: <bbl>${rdts}</bbl></div>` +
               `<div><b>Total kWh: ${tkhws}</b> | L1_kWh: ${l1khws} | L2_kWh: ${l2khws} | L3_kWh: ${l3khws}</div>`,
            spdiv = `<div class="sp-div">SYSPATH: ${sp}</div>`;
         /* -- */
         this.total_kwh = (tkhws == undefined) ? 0.0 : parseFloat(tkhws);
         let nullsty = "";
         if (tkhws == undefined)
            nullsty = "border-color: red !important; border-width: 2px;";
         /* -- */
         return `<div class="kwhs-reading" style="${nullsty}">${hdr}${bdy}${spdiv}</div>`;
      }
   }

};


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
