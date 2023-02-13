
class dbeditHtml {

   constructor() {
      this.disables = {"clients": ["dt_crd", "dt_del", "bitflags", "clt_rowid"]
         , "client_circuits": ["row_sid", "dt_link", "dt_unlink", "bitflags", "elec_met_cir_rowid"]
         , "elec_meter_circuits": ["*"]};
   }

   itemHtml(colinfo) {
      /* -- build item html -- */
      let chartypes = ["character varying", "character"]
         , numtypes = ["smallint", "integer"]
         , dtstype = ["date", "datetime"]
         , dbt = `dbtype=""`
         , mlen = ""
         , phldr=""
         , val = "";
      /* -- */
      if (chartypes.includes(colinfo.data_type)) {
         dbt = `dbtype="string"`;
      } else if (numtypes.includes(colinfo.data_type)) {
         dbt = `dbtype="number"`;
      } else if (dtstype.includes(colinfo.data_type)) {
         dbt = `dbtype="date"`;
      }
      /* -- */
      if (colinfo.column_default == null) {
         colinfo.column_default = "";
      }
      /* -- */
      if (colinfo.column_name == "elec_met_cir_rowid") {
         colinfo.column_default = "nextval";
         colinfo.is_nullable = "NO";
         dbt = `dbtype="auto"`;
         val = "auto";
      }
      /* -- */
      if (colinfo.column_default.startsWith("nextval")) {
         phldr = "auto";
         val = phldr;
      } else {
         phldr = colinfo.column_name;
      }
      /* -- */
      let dis = "", 
         curr_tbl_diss = this.disables[_omms.dbedit.current_table];
      if (curr_tbl_diss.includes(colinfo.column_name) || curr_tbl_diss[0] == "*")
         dis = `disabled="disabled"`;
      /* -- */
      _omms.dblbls.setLangTable(window.navigator.language, _omms.dbedit.current_table);
      let col_lbl = _omms.dblbls.getColLbl(colinfo.column_name)
         , lbltag = `<div class="lbl">${col_lbl}</div>`
         , nul = `null="${colinfo.is_nullable}"`
         , pl = `placeholder="${phldr}"`;
      /* -- */
      let inputbox = `<input id="COL_${colinfo.column_name}" type="text" value="${val}"` + 
            ` ${mlen} ${nul} ${dis} ${pl} ${dbt} />`;
      /* -- */
      return `<div class="input_ln">${lbltag}${inputbox}</div>`;
   }

   editorCRUDControls(tblname) {
      /* -- */
      if (tblname == "elec_meter_circuits")
         return "";
      /* -- */ 
      let html = `<div id="btnClear" class="crud-btn">Clear</div>` + 
         `<div id="btnUpsert" class="crud-btn">Upsert</div>` +
         `<div id="btnDelete" class="crud-btn">Delete</div>` + 
         `<input type="text" id="txtValidate" value="" placeholder="cba321" />` + 
         `<input type="hidden" id="txtTableName" value="${tblname}" />`;
      /* -- */
      return `<div id="tbl_${tblname}" class="crud-frame">${html}</div>`
   }

};
