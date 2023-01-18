
var dlSrcUrls = {
   client_tag: "href:/api/get/datalists/client-tags",
   circuit_tag: "href:/api/get/datalists/circuit-tags",
   building_tags: "href:/api/get/datalists/building-tags",
   fetch_client_tag: "href:/api/get/fetchcol/reports.clients/client_tag",
   fetch_circuit_tag: "href:/api/get/fetchcol/config.circuits/circuit_tag",
   fetch_builing_tag: "href:/api/get/fetchcol/config.org/entag|building",
   fetch_space_tag: "href:/api/get/fetchcol/reports.spaces/space_tag",
   floors: `json:{"Parking2": -2, "Parking1": -1, "Gound": 0, "1st Floor": 1` + 
      `, "2nd Floor": 2, "3rd Floor": 3, "4th Floor": 4, "5th Floor": 5, "NotSet": 999}`
};


var dlSources = {
   /* - - */
   tbls: {client_space_circuits: {entag: dlSrcUrls.building_tags,
            circuit_tag: dlSrcUrls.circuit_tag,
            client_tag: dlSrcUrls.client_tag,
            space_tag: dlSrcUrls.fetch_space_tag,
            status: `json:{"off": 0, "on": 1}`},
      /* - - */
      meters: {elcrm_entag: "href:/api/get/datalists/elcrm-tags"}, 
      clients: {client_tag: dlSrcUrls.fetch_client_tag},
      circuits: {circuit_tag: dlSrcUrls.fetch_circuit_tag, 
         entag: dlSrcUrls.fetch_builing_tag},
      spaces: {building_entag: dlSrcUrls.fetch_builing_tag,
         space_tag: dlSrcUrls.fetch_space_tag,
         floor: dlSrcUrls.floors}},
   /* - - */
   get(tblname, colname) {
      let tbl = this.tbls[tblname];
      if (tbl == undefined) 
         return null;
      let colval = tbl[colname];
      if (colval == undefined) 
         return null;
      /* - - */
      let id = `dl_${tblname}_${colname}`;
      return this.laod(id, colval);
   },

   laod(id, colval) {
      /* - - */
      let buff = dbTableHtml.dataList(id),
            selector = `#${id}`; 
         $(selector).remove();
         $("body").append(buff);
      /* - - */
      if (colval.startsWith("json:")) {
         let jobj = JSON.parse(colval.replace("json:", ""));
         /* - - */
         for (let p in jobj) {
            let v = jobj[p],
               opt = `<option p="${p}" v="${v}" value="${v} :: ${p}">`;
            $(selector).append(opt);
         }
         /* - - */
         selOut = selector;
      } else if (colval.startsWith("href:")) {
         /* - - */
         let __callback__ = function(jarr) {
               for (let idx in jarr) {
                  let obj = jarr[idx],
                     opt = `<option dbid="${obj.dbid}" value="${obj.xtag} :: ${obj.xdescr}">`;
                  $(selector).append(opt);
               }
            };
         /* - - */
         let __fetchcol__ = function(jarr) {
               for (let idx in jarr) {
                  let obj = jarr[idx],
                     opt = `<option dbid="${obj.tag}" value="${obj.tag}">`;
                  $(selector).append(opt);
               }
            };
         /* - - */
         let api = new restAPI(),
            url = colval.replace("href:", "");
         /* - - */
         if (url.includes("fetchcol"))
            __callback__ = __fetchcol__;
         /* - - */
         api.getDatalist(url, __callback__);
      }
      /* - - */
      return id;
   }
};


class databaseTable {

   static checkField(input, tblinfo) {
      /* - - */
      let id = $(input).attr("id"),
         colinfo = tblinfo.find(i => i.colname == id);
      /* - - */         
      return (id == colinfo.colname);
   }

   static checkOpCode() {
      let code = $("#dbTableOpCode").val();
      if (code != "a1b2") {
         alert("Bad or Missing DataOp Code!");
         $("#dbTableOpCode").val("")
         return false;
      } else {
         $("#dbTableOpCode").val("");
         return true;
      }
   }

   static attachDatalist(item) {
      let id = $(item).attr("id"),
         tbl = $(item).attr("tbl");
      let selector = dlSources.get(tbl, id);
      $(item).attr("list", selector);
   }

   static getTableInputFormData() {
      /* - - */
      let data = {}, 
         boolVal = false,
         okInputs = [], erInputs = [],
         selector = "form#dbTableForm",
         tbl = $(selector).attr("tbl"),
         tblinfo = app.tblInfos[tbl];
      /* - - */
      selector = `form#dbTableForm input[type="text"]`;
      $(selector).each(function(_, i) {
            boolVal = databaseTable.checkField(i, tblinfo);
            if (boolVal){
               okInputs.push(i);
            } else {
               erInputs.push(i);
            }
         });
      /* -- check for errors -- */
      if (erInputs.length > 0) {
         alert("input errors");   
      } else {
         /* -- set table index -- */
         data["tbl"] = tbl;
         okInputs.forEach(function(i) {
               let id = $(i).attr("id"), 
                  val = $(i).val();
               data[id] = val;
            });
      }
      /* - - */
      return databaseTable.prep4table(data);
   }

   static prep4table(data) {
      /* - - */
      let sep = "::";
      let cnt = function(str) {
            return str.split(sep).length;
         };
      /* - - */
      console.log(data);
      if (data.tbl == "client_space_circuits") {
         if (cnt(data.client_tag) == 2)
            data.client_tag = data.client_tag.split(sep)[0].trim();
         if (cnt(data.circuit_tag) == 2)
            data.circuit_tag = data.circuit_tag.split(sep)[0].trim();
         /* dirty fix for now */
         // data.circuit_tag = data.circuit_tag.replace("/", "_$_");
         if (cnt(data.bitflag) == 2)
            data.bitflag = parseInt(data.status.split(sep)[0].trim());
         if (cnt(data.entag) == 2)
            data.entag = data.entag.split(sep)[0].trim();
         if (cnt(data.space_tag) == 2)
            data.space_tag = data.space_tag.split(sep)[0].trim();
      }
      /* - - */
      return data;
   }

   constructor(jsonObj) {
      this.jsonObj = jsonObj;
      /* disabled table fields */
      this.disabled = { 
            client_space_circuits: ["bitflag"]
            , "0x02": []
            , meters: ["edge_name", "bus_type", "bus_address", "meter_type"
               , "meter_maker", "meter_model", "elcrm_entag"]
            , "0x06": []
            , "0x08": []
            , "0x10": []
         }
   }

   isColDisabled(tblIdx, colName) {
      let tbl = this.disabled[tblIdx];
      if (tbl == undefined)
         return false;
      /* - - */
      return tbl.includes(colName);
   }

   updateInputForm(jobj) {
      $("form#dbTableForm input").each((_, i) => {
            let id = $(i).attr("id");
            $(i).val(jobj[id]); 
         });
   }

   attachFilter() {
      $("#txtObjSelFilter").on("keydown", this.dbObjSelectorFilter);
   }

   attachUpsertNewDelete(upsert = true, xnew = true, xdelete = true) {
      /* - - */
      let sel = ".input-frm-btns input[id^=upsert]";
      $(sel).off().on("click", this.upsertRow);
      if (!upsert)
         $(sel).attr("disabled", "disabled");
      /* - - */
      sel = ".input-frm-btns input[id^=newrow]";
      $(sel).off().on("click", this.newRow);
      if (!xnew)
         $(sel).attr("disabled", "disabled");
      /* - - */
      sel = ".input-frm-btns input[id^=delrow]";
      $(sel).off().on("click", this.deleteRow);
      if (!xdelete) {
         $(sel).attr("disabled", "disabled");
         $("#delCode").attr("disabled", "disabled");
      }
      /* - - */
   }

   attachDatalists() {
      /* - - */
      let selector = "#dbTableForm input:enabled",
         keys = ["_tag", "entag", "status", "floor"];
      /* - - */
      $(selector).each((_, i) => {
            let id = $(i).attr("id");
            keys.forEach((key, _) => {
                  if (id.includes(key))
                     databaseTable.attachDatalist(i);
               });
         });
      /* - - */
   }

   dbObjSelectorFilter() {
      let val = this.value.trim().toUpperCase(),
         selector = "#dbObjSelector .clt-sel-item";
      /* - - */
      $(selector).each((_, item) => {
            let txt = $(item).text().toUpperCase();
            if (txt.includes(val) || (val == ""))
               $(item).css("display", "block");
            else
               $(item).css("display", "none");
         });
   }

   upsertRow() {
      /* -- check op code -- */
      if (!databaseTable.checkOpCode())
         return;
      /* - - */
      let data = databaseTable.getTableInputFormData(),
         api = new restAPI();
      /* - - */
      api.upsertConfigTable(data, function(jobj) {
            console.log([data, jobj]);
            submenuNav.clickLastClickedSubmenu();
         });
      /* - - */
   }

   newRow() {
      /* - - */
      let selector = `form#dbTableForm input[type="text"]`;
      $(selector).each((_, i) => {
            let coldef = $(i).attr("coldef");
            if (coldef) {
               $(i).val(coldef);
            } else {
               $(i).val("");
            }
         });
   }

   deleteRow() {
      /* -- check op code -- */
      if (!databaseTable.checkOpCode())
         return;
      /* - - */
      let api = new restAPI(), 
         data = databaseTable.getTableInputFormData();
      /* - - */
      api.deleteConfigRow(data, (jobj) => {
            console.log(jobj);
            submenuNav.clickLastClickedSubmenu();
         });
      /* - - */
   }

}
