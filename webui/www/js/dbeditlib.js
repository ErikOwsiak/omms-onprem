
class dbElecMeterCircut {

   /* t.met_cir_rowid
      , t.met_syspath
      , mm.model_string as met_model_rowid
      , t.met_note
      , t.elec_room_locl_tag as met_loc_rm
      , cast(t.met_dt_crd as varchar) as met_dt_crd
      , t.cir_tag
      , t.cir_amps
      , t.cir_volts
      , t.cir_locl_tag
      , t.cir_note
      , cast(t.cir_dt_crd as varchar) as cir_dt_crd */

   /* m_locl_tag, this.m_locl_tag = m_locl_tag; */
   constructor([rowid, syspath, mm_str, m_note, elc_room, m_dt_crd
         , cir_tag, amps, vol, cir_locl_tag, cir_dt_crd]) {
      /* -- */
      this.rowid = rowid;
      this.syspath = syspath;
      this.mm_str = mm_str;
      this.m_note = m_note;
      this.elc_room = (elc_room == null) ? "n/a" : elc_room;
      this.m_dt_crd = m_dt_crd;
      this.cir_tag = cir_tag;
      this.cir_amps = amps;
      this.cir_vol = vol;
      /* -- */
      this.cir_locl_tag = 
         (cir_locl_tag == null || cir_locl_tag == "") ? "n/a" : cir_locl_tag;
      /* -- */
      this.cir_dt_crd = cir_dt_crd;
      /* -- */
   }

   toHtml() {
      let row = `<div class="syspath">SYSPATH:&nbsp;<i>${this.syspath}</i></div>` +
         `<div class="mmstr">MET_STR:&nbsp;${this.mm_str}</div>` + 
         `<div>ELEC_ROOM:&nbsp;<b>${this.elc_room}</b></div>` + 
         `<div>CIRCUIT:&nbsp;<b>${this.cir_tag}</b></div>` + 
         `<div><bb>CIRCUIT_LOCALE:&nbsp;${this.cir_locl_tag}</bb></div>`;
      /* -- */
      return `<div class="lst-item-clt" rowid="${this.rowid}">${row}</div>`;
   }

}


class dbClient {
   
   constructor([rowid, tag, name, pin, phone, email, note, flags, dt_c, dt_d]) {
      this.rowid = rowid;
      this.tag = tag;
      this.name = name;
      this.pin = pin;
      this.phone = phone;
      this.email = email;
      this.note = note;
      this.flags = flags;
      this.dt_crd = dt_c;
      this.dt_del = dt_d;
   }
   
   toHtml() {
      let row = `<div>TAG (nip, taxid):&nbsp;<b>${this.tag}</b>` + 
         `</div><div><cln>${this.name}</cln></div>`;
      return `<div class="lst-item-clt" tag="${this.tag}">${row}</div>`;
   }
};


class dbClientMetCer {
   
   constructor([serid, tag, name, syspath, locl, cir, code, flags, dt_c, dt_d]) {
      this.rowid = serid;
      this.clttag = tag;
      this.cltname = name;
      this.syspath = syspath;
      this.locltag = locl;
      this.cirtag = cir;
      this.code = code;
      this.bitflags = flags;
      this.dt_lnk = dt_c;
      this.dt_ulnk = dt_d;
      /* -- */
   }

   toHtml() {
      let row = `<div class="syspath">SPATH:&nbsp;<i>${this.syspath}</i></div>` + 
         `<div>LOCALE:&nbsp;<b>${this.locltag}</b></div>` + 
         `<div>CIRCUIT:&nbsp;<b>${this.cirtag}</b></div>` + 
         `<div><bb>${this.cltname}</bb></div>`;
      return `<div class="lst-item-clt" rowid="${this.rowid}">${row}</div>`;
   }

};


_omms.Ser4 = "Serial4";
_omms.NotImp = "NotImplemented";


_omms.dblbls = {

   setLangTable(lng, tbl) {
      // console.log([lng, tbl]);
      if (lng.includes("en")) {
         this.lng = "en";
      } else if (lng.contains("pl")) {
         this.lng = "pl";
      } else if (lng.contains("de")) {
         this.lng = "de";
      } else {
         this.lng = "en";
      }
      /* -- */
      this.lng = "en";
      this.tbl = tbl;
      this.tbl_lbls = this.lbls[this.lng][this.tbl];
      // console.log(this); 
      /* -- */
   },

   getColLbl(colname) {
      if (this.tbl_lbls) {
         let lbl = this.tbl_lbls[colname];
         // console.log(lbl);
         return lbl;
      } else {
         return "LblNotFound";
      }
   },

   lbls: {"en": {
      elec_meter_circuits: {"met_cir_rowid": _omms.Ser4, "met_syspath": "Meter SYSPATH"
         , "met_model_rowid": "Meter String", "met_locl_tag": "Meter Electric Room TAG"
         , "met_note": "Meter Note", "met_dt_crd": "Date Meter Added", "cir_tag": "Circuit TAG"
         , "cir_amps": "Circuit AMPS", "cir_volts": "Circuit Volts"
         , "cir_locl_tag": "Circuit Clinet Location TAG", "cir_note": "Circuit Note"
         , "cir_dt_crd": "Date Circuit Added"},
      clients: {"clt_rowid": _omms.Ser4, "clt_tag": "Client tag: NIP, TaxID", "clt_name": "Client Name"
         , "clt_access_pin": "Client Access PIN code", "clt_phone": "Client's Phone Number"
         , "clt_email": "Clinet's Email Address", "note": "Note About the Client"
         , "bitflags": _omms.NotImp, "dt_crd": "Date Client Added", "dt_del": "Date Client Deleted"},
      client_circuits: {"row_sid": _omms.Ser4, "clt_tag": "Client tag: NIP, TaxID"
         , "locl_tag": "Client's locale TAG", "code": "Python code used with reports & etc.."
         , "bitflags": _omms.NotImp, "dt_link": "Date meter was liked to the client"
         , "cir_tag": "Circuit Tag", "elec_met_cir_rowid": _omms.Ser4
         , "dt_unlink": "Date meter was unliked from the client"}
      },

      "pl": {
      },

      "de": {
      }
   }
};
