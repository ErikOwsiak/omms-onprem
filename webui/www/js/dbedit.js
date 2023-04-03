
_omms.dbedit = null;


class dbEdit {

   constructor() {
      this.server = null;
      this.sessCache = {
            "tables": {}, dbObjs: {}
         };
      this.current_table = null;
   }

   init() {
      //$("#systemSettings").off().on("click", this.getTableInfo);
   }

   tblOnClick(tblname) {
      if (tblname in this.sessCache.tables) {
         let tinfo = this.sessCache.tables[tblname];
         console.log(tinfo);
      } else {

      }
   }

   getTableInfo(tblname) {
      this.current_table = tblname;
      if (tblname in this.sessCache.tables) {
         this.onGetTableInfo(tblname);
      } else {
         let __dbedit = this,
            url = `ui/dbedit/get/table/info?tbl=${tblname}`;
         $.get(url, function (res) {
               __dbedit.sessCache.tables[tblname] = res;
               __dbedit.onGetTableInfo(tblname);
            });
      }
   }

   onGetTableInfo(tblname) {
      /* -- */
      let dbhtml = new dbeditHtml();
      let ctrls = dbhtml.editorCRUDControls(tblname), 
         id_dbItemList = "newDBItemForm",
         html = `<div class="tbl_hdr">${tblname}</div>` +
            `<div id="${id_dbItemList}" class="new-dbitem-from"></div>` +
            `<div id="dbControls" class="db_controls">${ctrls}</div>`;
      /* -- */
      $("#dbEditorFrmRtCol").html(html);
      this.loadNewDBItemForm(id_dbItemList, tblname);
      /* attach btns events */
      let _this = this;
      $(".crud-btn").off().on("click", function() {
            /* -- */
            let btns = ["btnUpsert", "btnDelete"], 
               validate = $("#txtValidate").val();
            if (btns.includes(this.id) && validate != "cba321") {
               alert("Enter Validate Code!");
               return;
            }
            /* -- */
            switch (this.id) {
               case "btnClear":
                  _this.loadNewDBItemForm(id_dbItemList, tblname);
                  break;
               case "btnUpsert":
                  _this.upsertDBItem();
                  break;
               case "btnDelete":
                  _this.deleteDBItem();
                  break;
               default:
                  break;
            }
            /* -- */
         });
      /* clear db items list */
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
      let _this = this, itemObj;
      $.get(`ui/dbedit/get/${tblname}`, function (jsarr) {
         _this.sessCache.dbObjs[tblname] = {};
         jsarr.forEach((i) => {
               itemObj = new dbClient(i);
               _this.sessCache.dbObjs[tblname][itemObj.tag] = itemObj;
               $("#dbObjSelector").append(itemObj.toHtml());
            });
         /* -- */
         $("div.lst-item-clt").off().on("click", function () {
               let TAG_AS_ROWID = $(this).attr("tag");
               _this.onDatabaseItemObjectClick(TAG_AS_ROWID, tblname)
            });
         /* -- */
      });
   }

   getTblData_client_circuits(tblname) {
      let _this = this;
      this.loadDatalists();
      $.get(`ui/dbedit/get/${tblname}`, function (jsarr) {
         _this.sessCache.dbObjs[tblname] = {};
         jsarr.forEach((i) => {
               let itemObj = new dbClientMetCer(i);
               _this.sessCache.dbObjs[tblname][itemObj.rowid] = itemObj;
               $("#dbObjSelector").append(itemObj.toHtml());
            });
         /* -- onclick -- */
         $("div.lst-item-clt").off().on("click", function () {
               let ROWID = $(this).attr("rowid");
               _this.onDatabaseItemObjectClick(ROWID, tblname);
            });
         /* -- */
      });
   }

   getTblData_elec_meter_circuits(tblname) {
      let _this = this;
      $.get(`ui/dbedit/get/${tblname}`, function (jsarr) {
         _this.sessCache.dbObjs[tblname] = {};
         jsarr.forEach((i) => {
            let itemObj = new dbElecMeterCircut(i);
            _this.sessCache.dbObjs[tblname][itemObj.rowid] = itemObj;
            $("#dbObjSelector").append(itemObj.toHtml());
         });
         /* -- */
         $("div.lst-item-clt").off().on("click", function () {
            let ROWID = $(this).attr("rowid");
            _this.onDatabaseItemObjectClick(ROWID, tblname);
         });
      });
   }

   displayNewItemForm(dbItemList, tblinfo) {
      /* -- */
      $(`#${dbItemList}`).html("");
      let dbhtml = new dbeditHtml();
      tblinfo.forEach((i) => {
            let _html = dbhtml.itemHtml(i);
            $(`#${dbItemList}`).append(_html);
         });
      let selectors = "#COL_clt_tag, #COL_locl_tag, #COL_cir_tag, #COL_clt_name";
      /* -- */
      if (!($(selectors).parent().hasClass("must_fill"))) {
         $(selectors).parent().addClass("must_fill");
         $(selectors).siblings().append("&nbsp;&nbsp;<small>*( required )</small>");
      }
      /* -- */
      this.loadDatalists();
   }

   onDatabaseItemObjectClick(ITEM_INDEX, tblname) {
      let ns = "#dbEditorFrmRtCol",
         itemObj = this.sessCache.dbObjs[tblname][ITEM_INDEX];
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
               $(`${ns} #COL_clt_tag`).attr("disabled", "1");
               $(`${ns} #COL_clt_name`).val(itemObj.name);
               $(`${ns} #COL_clt_access_pin`).val(itemObj.pin);
            }
            break;
         case "client_circuits":
            {
               $(`${ns} #COL_row_sid`).val(itemObj.rowid);
               $(`${ns} #COL_bitflags`).val(itemObj.bitflags);
               $(`${ns} #COL_dt_link`).val(itemObj.dt_lnk);
               $(`${ns} #COL_dt_unlink`).val(itemObj.dt_ulnk);
               $(`${ns} #COL_code`).val(itemObj.code);
               $(`${ns} #COL_clt_tag`).val(itemObj.clttag);
               $(`${ns} #COL_clt_tag`).attr("disabled", "1");
               $(`${ns} #COL_locl_tag`).val(itemObj.locltag);
               $(`${ns} #COL_cir_tag`).val(itemObj.cirtag);
            }
            break;
         case "elec_meter_circuits":
            {
               $(`${ns} #COL_met_cir_rowid`).val(itemObj.rowid);
               $(`${ns} #COL_met_syspath`).val(itemObj.syspath);
               $(`${ns} #COL_met_model_rowid`).val(itemObj.mm_str);
               $(`${ns} #COL_met_dt_crd`).val(itemObj.m_dt_crd);
               $(`${ns} #COL_cir_amps`).val(itemObj.cir_amps);
               $(`${ns} #COL_cir_volts`).val(itemObj.cir_vol);
               $(`${ns} #COL_cir_dt_crd`).val(itemObj.cir_dt_crd);
               $(`${ns} #COL_cir_tag`).val(itemObj.cir_tag);
               $(`${ns} #COL_met_note`).val(itemObj.m_note);
               $(`${ns} #COL_cir_note`).val("cirnote");
            }
            break;
         default:
            break;
      }
   }

   loadNewDBItemForm(id_dbItemList, tblname) {
      let tblinfo = this.sessCache.tables[tblname];
      this.displayNewItemForm(id_dbItemList, tblinfo);
   }

   deleteDBItem() {
      let tblname = $("#txtTableName").val(),
         rowidstr = "";
      if (tblname == "clients") {
         rowidstr = "COL_clt_rowid"
      } else if (tblname == "client_circuits") {
         rowidstr = "COL_row_sid"
      } else {
         alert(`BadTableName: ${tblname}`);
         return;
      }
      /* -- */
      let rowid = $(`#newDBItemForm #${rowidstr}`).val(), 
         url = `ui/dbedit/delete?tbl=${this.current_table}&rowid=${rowid}`;
      let data = {"rowid": rowid};
      $.delete(url, data, function(res) {
            if (res.ErrorMsg == "OK")
               alert(`Record Deleted OK`);
            else
               alert(`Record Delete Error\n${res.ErrorMsg}`);
            /* -- */
            $("#settingsClient").click();
         });
   }

   upsertDBItem() {
      let data = {};
      $("#newDBItemForm input").each((_, i) => {
            data[i.id] = $(i).val();
         });
      /* -- */
      let url = `ui/dbedit/upsert?tbl=${this.current_table}`;
      $.post(url, data, function(res) {
            if (res.ErrorMsg == "OK")
               alert(`Record Upsert OK`);
            else
               alert(`Record Upsert Error\n${res.ErrorMsg}`);
            /* -- */
            $("#settingsClient").click();
         });
   }

   loadDatalists() {
      let url = "ui/dbedit/get_datalists",
         _this = this;
      /* -- */
      $.get(url, function(jsobj) {
            _this.datalists = null;
            _this.datalists = jsobj;
            _this.createDatalists();
            _this.attachDatalists();
         });
      /* -- */
   }

   createDatalists() {
      /* -- */
      let createlst = function(key, items) {
            let dlid = `dl_${key}`;
            $("div#datalists").append(`<datalist id="${dlid}" />`);
            items.forEach((item) => {
                  switch (key) {
                     case "clts":
                        {
                           let [rowid, clttag, cltname] = item;
                           let val = `${rowid} :: ${clttag} :: ${cltname}`;
                           $(`#${dlid}`).append(`<option value="${val}">`);
                        }
                        break;
                     case "cirs":
                        {
                           let [rowid, cirtag] = item;
                           let val = `${rowid} :: ${cirtag}`;
                           $(`#${dlid}`).append(`<option value="${val}">`);
                        }
                        break;
                     case "locs":
                        {
                           let [rowid, bldtag, loctag] = item;
                           let val = `${rowid} :: ${bldtag} :: ${loctag}`;
                           $(`#${dlid}`).append(`<option value="${val}">`);
                        }
                        break;
                     default:
                        break;
                  }
               });
         };
      /* -- */
      if ($("div#datalists").length > 0)
         $("div#datalists").remove();
      /* -- */
      $("body").append(`<div id="datalists" />`);
      /* -- */
      for (let key in this.datalists)
         createlst(key, this.datalists[key]);
      /* -- */
   }

   attachDatalists() {
      let d = {"COL_clt_tag": "dl_clts"
         , "COL_locl_tag": "dl_locs", "COL_cir_tag": "dl_cirs"};
      /* -- */
      for (let key in d) {
         console.log([key, d[key]]);
         $(`#${key}`).attr("list", d[key]);
      }
   }
};
