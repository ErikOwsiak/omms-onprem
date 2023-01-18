

var dbTableLbls = {
   /* - - */
   tbls: {"client_spaces": {entag: "building_entag"}
      , "meters": {"elcrm_entag": "electrical_room_entag"}
      , "circuits": {entag: "building_entag"}
      , "client_circuits": {entag: "building_entag"}},
   /* - - */
   get(tblname, colname) {
      let tbl = this.tbls[tblname];
      if (tbl == undefined)
         return colname;
      let lbl = tbl[colname];
      if (lbl == undefined)
         return colname;
      /* - - */
      return lbl;
   }
};


var dbTableHtml = {

   getClinetSelectorItem(obj) {
      let jbuff = encodeURIComponent(JSON.stringify(obj));
      return `<div class="clt-sel-item" jsonbuff="${jbuff}">` + 
         `<div><b>${obj.client_name}</b></div><div>tag/nip: ${obj.client_tag}</div></div>`;
   },

   getCircuitSelectorItem(obj) {
      let jbuff = encodeURIComponent(JSON.stringify(obj)),
         buff = `building: ${obj.entag}; voltage: ${obj.voltage}; amps: ${obj.max_amps}`;
      /* - - */
      return `<div class="clt-sel-item" jsonbuff="${jbuff}">` + 
         `<div><b>${obj.circuit_tag}</b></div><div>${buff}</div></div>`;
   },

   getCltCircuitSelectorItem(obj) {
      let jbuff = encodeURIComponent(JSON.stringify(obj)),
         buff = `building tag:&nbsp;<b>${obj.entag}</b>;&nbsp;` +
            `circuit_tag:&nbsp;<b>${obj.circuit_tag}</b>;` +
            `&nbsp;bitflag:&nbsp;<b>${obj.bitflag}</b>`;
      /* - - */
      return `<div class="clt-sel-item" jsonbuff="${jbuff}">` + 
         `<div><b>${obj.client_tag}</b>&nbsp;::&nbsp;<b>${obj.client_name}</b></div>` + 
         `<div>${buff}</div><div>space tag:&nbsp;<b>${obj.space_tag}</b></div></div>`;
   },

   getMeterSelectorItem(o) {
      let jbuff = encodeURIComponent(JSON.stringify(o)),
         mStr = `&nbsp;&nbsp;${o.elcrm_entag}::${o.edge_name}::${o.bus_type}::${o.bus_address}`,
         buff = `maker: ${o.meter_maker}; model: ${o.meter_model}; type: ${o.meter_type};`;
      /* - - */
      return `<div class="clt-sel-item" jsonbuff="${jbuff}">` + 
         `<div>meter string:<b>${mStr}</b></div><div>${buff}</div>` + 
         `<div>circuit tag:&nbsp;<b>${o.circuit_tag}</b></div></div>`;
   },

   getSpaceSelectorItem(o) {
      /* - - */
      let jbuff = encodeURIComponent(JSON.stringify(o)),
         floor = (o.floor) ? o.floor : "NotSet",
         area = (o.area_m2) ? parseFloat(o.area_m2).toFixed(1) : "NotSet",
         buff = `building entag: <b>${o.building_entag}</b>; area m2: <b>${area}</b>;` + 
            ` floor: <b>${floor}</b>;`;
      /* - - */
      return `<div class="clt-sel-item" jsonbuff="${jbuff}">` + 
         `<div>space tag:&nbsp;<b>${o.space_tag}</b></div>` +
         `<div>${buff}</div></div>`;
   },

   getRowInputForm(jsonColObj, tbl) {
      let head = `<div class="head-db-tbl-form">${tbl}</div>`  
         form = `<form id="dbTableForm" tbl="${tbl}">`,
         __out = [head, form];
      /* - - */
      for(let p in jsonColObj) {
         let obj = jsonColObj[p];
         obj.tbl = tbl;
         __out.push(this.__html(obj));
      }
      __out.push("</form>");
      __out.push(this.rowInputFormBtns(tbl));
      /* - - */
      return __out;
   },

   rowInputFormBtns(tbl) {
      /* - - */
      let btns = `<input id="upsert_${tbl}" tbl="${tbl}" type="button" value="upsert" />` + 
         `<input id="delrow_${tbl}" tbl="${tbl}" type="button" value="delete" />` +
         `<input id="dbTableOpCode" type="text" maxlength="4" />` + 
         `<input id="newrow_${tbl}" tbl="${tbl}" type="button" value="clear" />`;
      /* - - */
      return `<div class="input-frm-btns"><div class="ln-frm-btns">${btns}</div>` + 
         `<div id="dbFeedback" class="db-feedback"></div></div>`;
   },

   dataList(id) {
      return `<datalist id="${id}"></datalist>`;
   },

   __html(colObj) {
      switch(colObj.dtype) {
         case "character varying":
            return this.__varchar(colObj);
         case "integer":
            return this.__int(colObj);
         case "real":
            return this.__real(colObj);
         default:
            return "";
      }
   },

   __varchar(colObj) {
      /* - - */
      let tbl = colObj.tbl,
         colname = colObj.colname,
         lblname = dbTableLbls.get(tbl, colname);
      /* - - */
      if (colObj.coldef && colObj.coldef.startsWith("nextval")) {
         let __coldef = `${colObj.colname}::default`;
         return `<label>${lblname}</label>` + 
            `<input id="${colObj.colname}" type="text" value="${__coldef}"` + 
            ` class="db-input-txt" maxlength="${colObj.maxlen}" disabled tbl="${tbl}"` +
            ` coldef="${__coldef}" />`;
         /* - - */
      } else {
         /* - - */
         let disabled = app.__databaseTable.isColDisabled(tbl, colObj.colname),
            ds = (disabled) ? "disabled" : "";
         /* - - */
         return `<label>${lblname}</label>` + 
            `<input id="${colObj.colname}" type="text" class="db-input-txt"` + 
            ` placeholder="${colObj.colname}" maxlength="${colObj.maxlen}"` +  
            ` tbl="${tbl}" ${ds} />`;
         /* - - */
      }
   },

   __int(colObj) {
      /* - - */
      let tbl = colObj.tbl,
         colname = colObj.colname,
         lblname = dbTableLbls.get(tbl, colname);
      /* - - */
      if ((colObj.coldef != null) && (colObj.coldef.startsWith("nextval"))) {
         let __coldef = `${colObj.colname}::default`;
         return `<label>${lblname}</label>` + 
            `<input id="${colObj.colname}" type="text" value="${__coldef}"` +
            ` class="db-input-int" disabled tbl="${tbl}" coldef="${__coldef}" />`;
      } else {
         let disabled = app.__databaseTable.isColDisabled(tbl, colObj.colname);
         let ds = (disabled) ? "disabled" : "";
         return `<label>${lblname}</label>` + 
            `<input id="${colObj.colname}" type="text" class="db-input-int"` + 
            ` placeholder="${colObj.colname}" maxlength="${colObj.maxlen}"` + 
            ` tbl="${tbl}" ${ds} />`;
      }
   },

   __real(colObj) {
      /* - - */
      let tbl = colObj.tbl,
         colname = colObj.colname,
         lblname = dbTableLbls.get(tbl, colname);
      /* - - */
      if ((colObj.coldef != null) && (colObj.coldef.startsWith("nextval"))) {
         let __coldef = `${colObj.colname}::default`;
         return `<label>${lblname}</label>` + 
            `<input id="${colObj.colname}" type="text" value="${__coldef}"` +
            ` class="db-input-int" disabled tbl="${tbl}" coldef="${__coldef}" />`;
      } else {
         let disabled = app.__databaseTable.isColDisabled(tbl, colObj.colname);
         let ds = (disabled) ? "disabled" : "";
         return `<label>${lblname}</label>` + 
            `<input id="${colObj.colname}" type="text" class="db-input-real"` + 
            ` placeholder="${colObj.colname}" maxlength="16"` + 
            ` tbl="${tbl}" ${ds} />`;
      }
   }
   
};
