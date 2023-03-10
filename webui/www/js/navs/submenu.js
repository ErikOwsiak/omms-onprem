

class submenuNav {


   static lastClickedSubmenu = null;


   static clickLastClickedSubmenu() {
      try {
         let btnID = $(submenuNav.lastClickedSubmenu).attr("id"),
         funcName = `${btnID}Click`;
         /* make call */
         _omms.app.subNav[funcName](submenuNav.lastClickedSubmenu);
      } catch(e) {
         console.log(e);
      }
   }

   static createTable(jarr, tbl, upsert = true, xnew = true, xdelete = true) {
      let __out = dbTableHtml.getRowInputForm(jarr, tbl);
      $("#dbEditorFrmRtCol").html(__out.join(""));
      _omms.app.__databaseTable.attachUpsertNewDelete(upsert, xnew, xdelete);
      _omms.app.__databaseTable.attachDatalists();
   }

   static createSelectorListItem(jarr, htmlGenFunc) {
      $("#dbObjSelector").html("");
      jarr.forEach((i) => {
            let buff = htmlGenFunc(i);
            $("#dbObjSelector").append(buff);
         });
      /* - - */
      $("#dbObjSelector .clt-sel-item").off().on("click"
         , submenuNav.cltSelItemClick);
   }

   static cltSelItemClick() {
      let str = decodeURIComponent($(this).attr("jsonbuff")),
         jobj = JSON.parse(str),
         dbtbl = new databaseTable();
      /* - - */
      dbtbl.updateInputForm(jobj);
   };

   constructor(xmlFormName) {
      console.log("submenuNav:c-tor");
      this.xmlFormName = xmlFormName;
      let ns = `#subMenuCol #${this.xmlFormName}`, 
         selector = `${ns} navbtn:not(.greyout)`;
      $(selector).off().on("click", this.onSubmenuItemClick);
   }

   /* fired by a submenu buttons o on the right */
   onSubmenuItemClick() {
      let funcName = "";
      try {
         submenuNav.lastClickedSubmenu = this;
         let btnID = $(submenuNav.lastClickedSubmenu).attr("id");
         funcName = `${btnID}Click`;
         console.log(funcName);
         _omms.app.subNav[funcName](submenuNav.lastClickedSubmenu);
      } catch(e) {
         console.log([funcName, e]);
      }
   }

   kWhrsReportsClick() {
      _omms.gui.loadDataBlockXml("kWhrsRptFrame");            
   }

   settingsClientClick(__this) {
      /* - - */
      _omms.gui.loadDataBlockXml("databaseEditorFrame");
      let tbl = $(__this).attr("tbl"), api = new restAPI();
      _omms.dbedit.getTableInfo(tbl);
      /* - - */
   }

   settingsElecMeterCircuitsClick(__this) {
      _omms.gui.loadDataBlockXml("databaseEditorFrame");
      let tbl = $(__this).attr("tbl")
         , api = new restAPI();
      _omms.dbedit.getTableInfo(tbl);
   }

   monthPickerClick() {
      _omms.app.startMonthyReport();
   }

   // settingsMetersClick(__this) {
   //    /* load xml */
   //    _omms.gui.loadDataBlockXml("databaseEditorFrame");
   //    let api = new restAPI(),
   //       tbl = $(__this).attr("tbl");
   //    /* - - */
   //    let showUpsert = true, showNew = false, showDel = false;
   //    api.getTableInfo(tbl, function(jarr, tbl) {
   //          submenuNav.createTable(jarr, tbl, showUpsert, showNew, showDel);
   //       });
   //    /* - - */
   //    api.getMeters(2, function(jarr) {
   //          submenuNav.createSelectorListItem(jarr
   //             , dbTableHtml.getMeterSelectorItem);
   //       });
   //    /* - - */
   // }

   settingsSpacesClick(__this) {
      /* - - */
      _omms.gui.loadDataBlockXml("databaseEditorFrame");
      let tbl = $(__this).attr("tbl"),
         api = new restAPI();
      console.log(tbl);
      /* - - */
      api.getTableInfo(tbl, function(jarr, tbl) {
            submenuNav.createTable(jarr, tbl);
         });
      /* -- getTable(tbl, args, callback) -- */
      api.getTable("spaces", null, function(jarr) {
            submenuNav.createSelectorListItem(jarr
               , dbTableHtml.getSpaceSelectorItem);
         });
      /* - - */
   }

   settingsClientMeterCircuitsClick(__this) {
      /* - - */
      _omms.gui.loadDataBlockXml("databaseEditorFrame");
      let tbl = $(__this).attr("tbl"),
         api = new restAPI();
      /* - - */
      _omms.dbedit.getTableInfo(tbl);
   }

   to_delete_settingsClientSpaceCircuitsClick(__this) {
      /* - - */
      _omms.gui.loadDataBlockXml("databaseEditorFrame");
      let tbl = $(__this).attr("tbl"),
         api = new restAPI();
      /* - - */
      api.getTableInfo(tbl, function(jarr, tbl) {
            submenuNav.createTable(jarr, tbl);
         });
      /* - - */
      api.getClientCircuits(function(jarr) {
            submenuNav.createSelectorListItem(jarr, 
               dbTableHtml.getCltCircuitSelectorItem);
         });
      /* - - */
   }

   clientCircuitsHistoryClick(__this) {
      _omms.gui.loadDataBlockXml("clientCircuitHistory");
   }

   syspathsViewClick(__this) {
      /* load dynamic view */
      alert("NotImplemented");
   }
};
