
_omms.dbedit = null;


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
   
   constructor([rowid, tag, name, syspath, locl, cir, code, flags, dt_c, dt_d]) {
      this.rowid = rowid;
      this.clttag = tag;
      this.cltname = name;
      this.syspath = syspath;
      this.locltag = locl;
      this.cirtag = cir;
      this.code = code;
      this.bitflags = flags;
      this.dt_lnk = dt_c;
      this.dt_ulnk = dt_d;
   }

   toHtml() {
      let row = `<div class="syspath">SPATH:&nbsp;<i>${this.syspath}</i></div>` + 
         `<div>LOCALE:&nbsp;<b>${this.locltag}</b></div>` + 
         `<div>CIRCUIT:&nbsp;<b>${this.cirtag}</b></div>` + 
         `<div><bb>${this.cltname}</bb></div>`;
      return `<div class="lst-item-clt" rowid="${this.rowid}">${row}</div>`;
   }

};

class dbElecMeterCircut {
   
   constructor([rowid, syspath, mm, m_locl_tag, m_note, m_dt_crd, cir_tag,
         amps, vol, cir_locl_tag, cir_dt_crd]) {
      this.rowid = rowid;
      this.syspath = syspath;
      this.mm = mm;
      this.m_locl_tag = m_locl_tag;
      this.m_note = m_note;
      this.m_dt_crd = m_dt_crd;
      this.cir_tag = cir_tag;
      this.cir_amps = amps;
      this.cir_vol = vol;
      this.cir_locl_tag = cir_locl_tag;
      this.cir_dt_crd = cir_dt_crd;
   }

   toHtml() {
      let row = `<div class="syspath">SYSPATH:&nbsp;<i>${this.syspath}</i></div>` +
         `<div class="mmstr">METER_STR:&nbsp;${this.mm}</div>` + 
         `<div>METER_LOCALE:&nbsp;<b>${this.m_locl_tag}</b></div>` + 
         `<div>CIRCUIT:&nbsp;<b>${this.cir_tag}</b></div>` + 
         `<div><bb>CIRCUIT_LOCALE:&nbsp;${this.cir_locl_tag}</bb></div>`;
      return `<div class="lst-item-clt" rowid="${this.rowid}">${row}</div>`;
   }

}


class dbEdit {

   constructor() {
      this.server = null;
      this.sessCache = {
         "tables": {}, dbObjs: {}};
      this.disables = {"clients": ["dt_crd", "dt_del", "bitflags", "clt_rowid"]
         , "client_meter_circuits": ["dt_link", "dt_unlink", "bitflags", "elec_met_cir_rowid"]
         , "elec_meter_circuits": ["*"]};
      this.current_table = null;
   }

   init() {
      $("#systemSettings").off().on("click", this.getTableInfo);
   }

   tblOnClick(tblname) {
      if (tblname in this.sessCache.tables) {
         let tinfo = this.sessCache.tables[tblname];
         console.log(tinfo);
      } else {
         
      }
   }

   getTableInfo(tblname) {
      /* -- */
      this.current_table = tblname;
      if (tblname in this.sessCache.tables) {
         this.onGetTableInfo(tblname);
      } else {
         let __dbedit = this, 
            url = `/dbedit/get/table/info?tbl=${tblname}`;
         $.get(url, function(res) {
            __dbedit.sessCache.tables[tblname] = res;
               __dbedit.onGetTableInfo(tblname);
            });
      }
   }

   onGetTableInfo(tblname) {
      /* - - */
      let tblinfo = this.sessCache.tables[tblname]
         , clthdr = `<div class="tbl_hdr">${tblname}</div>`;
      $("#dbEditorFrmRtCol").html(clthdr);
      this.displayNewItemForm(tblinfo);
      $("#dbObjSelector").html("");
      /* -- start -- */
      let get_data_func = `getTblData_${tblname}`;
      try {
         this[get_data_func](tblname);
      } catch (e) {
         console.log([get_data_func, e]);
      }  
      /* -- end -- */
   }

   getTblData_clients(tblname) {
      let _this = this;
      $.get(`/dbedit/get/${tblname}`, function(jsarr) {
            _this.sessCache.dbObjs[tblname] = {};
            jsarr.forEach((i) => {
                  let itemObj = new dbClient(i);
                  _this.sessCache.dbObjs[tblname][itemObj.tag] = itemObj;
                  $("#dbObjSelector").append(itemObj.toHtml());
               });
            /* -- */
            $("div.lst-item-clt").off().on("click", function() {
                  let TAG_AS_ROWID = $(this).attr("tag");
                  _this.onDatabaseItemObjectClick(TAG_AS_ROWID, tblname)
               });
         });
   }

   getTblData_client_meter_circuits(tblname) {
      let _this = this;
      $.get(`/dbedit/get/${tblname}`, function(jsarr) {
            _this.sessCache.dbObjs[tblname] = {};
            jsarr.forEach((i) => {
                  let itemObj = new dbClientMetCer(i);
                  _this.sessCache.dbObjs[tblname][itemObj.rowid] = itemObj;
                  $("#dbObjSelector").append(itemObj.toHtml());
               });
            /* -- */
            $("div.lst-item-clt").off().on("click", function() {
                  let ROWID = $(this).attr("rowid");
                  _this.onDatabaseItemObjectClick(ROWID, tblname)
               });
         });
   }

   getTblData_elec_meter_circuits(tblname) {
      let _this = this;
      $.get(`/dbedit/get/${tblname}`, function(jsarr) {
            _this.sessCache.dbObjs[tblname] = {};
            jsarr.forEach((i) => {
                  let itemObj = new dbElecMeterCircut(i);
                  _this.sessCache.dbObjs[tblname][itemObj.rowid] = itemObj;
                  $("#dbObjSelector").append(itemObj.toHtml());
               });
            /* -- */
            $("div.lst-item-clt").off().on("click", function() {
                  let ROWID = $(this).attr("rowid");
                  _this.onDatabaseItemObjectClick(ROWID, tblname);
               });
         });
   }

   displayNewItemForm(tblinfo) {
      tblinfo.forEach((i) => {
            let _html = this.itemHtml(i);
            $("#dbEditorFrmRtCol").append(_html);
         });
   }

   itemHtml(i) {
      /* -- build item html -- */
      let diss = this.disables[this.current_table];
      let chartypes = ["character varying", "character"],
         numtypes = ["smallint", "integer"], ibtype = "text",
         mlen="", phldr="";
      /* -- -- */
      if (chartypes.includes(i.data_type)) {
         ibtype = "text"; 
         mlen=`maxlength="${i.character_maximum_length}"`;
      } else if (numtypes.includes(i.data_type)) {
         ibtype="number"; 
         mlen=`min="${0}" max="${i.character_maximum_length}"`;
      }
      /* -- */
      if (i.column_default == null) {
         i.column_default = "";
      }
      /* -- */
      let val = "";
      if (i.column_name == "elec_met_cir_rowid") {
         i.column_default = "nextval";
         val = "auto";
      }
      /* -- */
      if (i.column_default.startsWith("nextval")) {
         phldr = "auto";
         val = phldr;
      } else {
         phldr = i.column_name;
      }
      /* -- */
      let dis = "";
      if (diss.includes(i.column_name) || diss[0] == "*")
         dis = `disabled="disabled"`
      /* -- */
      let lbl = _omms.dbColdNames.en[i.column_name];
      if (lbl == undefined)
         lbl = "";
      let lbltag = `<div class="lbl">${lbl}</div>`, 
         nul = `null="${i.is_nullable}"`, pl = `placeholder="${phldr}"`,
         id = i.column_name,
         box = `<input id="COL_${id}" type="${ibtype}" value="${val}"` + 
            ` ${mlen} ${nul} ${dis} ${pl} />`;
      /* -- */
      return `<div class="input_ln">${lbltag}${box}</div>`;
   }

   onDatabaseItemObjectClick(ITEM_INDEX, tblname) {
      let ns = "#dbEditorFrmRtCol",
         itemObj = this.sessCache.dbObjs[tblname][ITEM_INDEX];
      console.log([ITEM_INDEX, tblname, itemObj])
      switch (tblname) {
         case "clients":
               { 
                  $(`${ns} #COL_clt_rowid`).val(itemObj.rowid);
                  $(`${ns} #COL_bitflags`).val(itemObj.flags);
                  $(`${ns} #COL_dt_crd`).val(itemObj.dt_crd);
                  $(`${ns} #COL_dt_del`).val(itemObj.dt_del);
                  $(`${ns} #COL_clt_phone`).val(itemObj.phone);
                  $(`${ns} #COL_clt_email`).val(itemObj.email);
                  $(`${ns} #COL_note`).val(itemObj.note);
                  $(`${ns} #COL_clt_tag`).val(itemObj.tag);
                  $(`${ns} #COL_clt_name`).val(itemObj.name);
                  $(`${ns} #COL_clt_access_pin`).val(itemObj.pin);
               }
            break;
         case "client_meter_circuits":
               {
                  $(`${ns} #COL_elec_met_cir_rowid`).val(itemObj.rowid);
                  $(`${ns} #COL_bitflags`).val(itemObj.bitflags);
                  $(`${ns} #COL_dt_link`).val(itemObj.dt_lnk);
                  $(`${ns} #COL_dt_unlink`).val(itemObj.dt_ulnk);
                  $(`${ns} #COL_code`).val(itemObj.code);
                  $(`${ns} #COL_clt_tag`).val(itemObj.clttag);
                  $(`${ns} #COL_locl_tag`).val(itemObj.locltag);
                  $(`${ns} #COL_cir_tag`).val(itemObj.cirtag);
               } 
            break;
         case "elec_meter_circuits":
               { 
                  $(`${ns} #COL_met_cir_rowid`).val(itemObj.rowid);
                  $(`${ns} #COL_met_model_rowid`).val(itemObj.flags);
                  $(`${ns} #COL_met_dt_crd`).val(itemObj.m_dt_crd);
                  $(`${ns} #COL_cir_amps`).val(itemObj.cir_amps);
                  $(`${ns} #COL_cir_volts`).val(itemObj.cir_vol);
                  $(`${ns} #COL_cir_dt_crd`).val(itemObj.cir_dt_crd);
                  $(`${ns} #COL_cir_tag`).val(itemObj.cir_tag);
                  $(`${ns} #COL_met_syspath`).val(itemObj.syspath);
                  $(`${ns} #COL_met_note`).val(itemObj.m_note);
                  $(`${ns} #COL_cir_note`).val("cirnote");
               }
            break;
         default:
            break;
      }
   }
};
