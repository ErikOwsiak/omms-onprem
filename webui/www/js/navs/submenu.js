
class submenuNav {

   static lastClickedSubmenu = null;

   static clickLastClickedSubmenu() {
      try {
         let btnID = $(submenuNav.lastClickedSubmenu).attr("id"),
         funcName = `${btnID}Click`;
         /* make call */
         app.subNav[funcName](submenuNav.lastClickedSubmenu);
      } catch(e) {
         console.log(e);
      }
   }

   static createTable(jarr, tbl, upsert = true, xnew = true, xdelete = true) {
      let __out = dbTableHtml.getRowInputForm(jarr, tbl);
      $("#dbEditorFrmRtCol").html(__out.join(""));
      app.__databaseTable.attachUpsertNewDelete(upsert, xnew, xdelete);
      app.__databaseTable.attachDatalists();
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
      this.xmlFormName = xmlFormName;
      console.log("submenuNav:c-tor");
      let selector = `#${this.xmlFormName} navbtn:not(.greyout)`;
      $(selector).off().on("click", this.onItemClick);
   }

   /* fired by a submenu button */
   onItemClick() {
      try {
         /* - - */
         submenuNav.lastClickedSubmenu = this;
         let btnID = $(submenuNav.lastClickedSubmenu).attr("id"),
            funcName = `${btnID}Click`;
         /* - - */
         console.log(funcName);
         app.subNav[funcName](submenuNav.lastClickedSubmenu);
         /* - - */
      } catch(e) {
         console.log(e);
      }
   }

   kWhrsReportsClick() {
      gui.loadDataBlockXml("kWhrsRptFrame");            
   }

   settingsClientClick(__this) {
      /* - - */
      gui.loadDataBlockXml("databaseEditorFrame");
      let tbl = $(__this).attr("tbl"),
         api = new restAPI();
      /* - - */
      api.getTableInfo(tbl, function(jarr, tbl) {
            submenuNav.createTable(jarr, tbl);
         });
      /* - - */
      api.getClients(function(jarr) { 
            submenuNav.createSelectorListItem(jarr
               , dbTableHtml.getClinetSelectorItem);
         });
      /* - - */
   }

   settingsCircuitClick(__this) {
      /* - - */
      gui.loadDataBlockXml("databaseEditorFrame");
      let tbl = $(__this).attr("tbl"),
         api = new restAPI();
      /* - - */
      api.getTableInfo(tbl, function(jarr, tbl) {
            submenuNav.createTable(jarr, tbl);
         });
      /* - - */
      api.getCircuits(function(jarr) { 
            submenuNav.createSelectorListItem(jarr
               , dbTableHtml.getCircuitSelectorItem);
         });
      /* - - */
   }

   settingsMetersClick(__this) {
      /* load xml */
      gui.loadDataBlockXml("databaseEditorFrame");
      let api = new restAPI(),
         tbl = $(__this).attr("tbl");
      /* - - */
      let showUpsert = true, showNew = false, showDel = false;
      api.getTableInfo(tbl, function(jarr, tbl) {
            submenuNav.createTable(jarr, tbl, showUpsert, showNew, showDel);
         });
      /* - - */
      api.getMeters(2, function(jarr) {
            submenuNav.createSelectorListItem(jarr
               , dbTableHtml.getMeterSelectorItem);
         });
      /* - - */
   }

   settingsSpacesClick(__this) {
      /* - - */
      gui.loadDataBlockXml("databaseEditorFrame");
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

   settingsClientSpaceCircuitsClick(__this) {
      /* - - */
      gui.loadDataBlockXml("databaseEditorFrame");
      let tbl = $(__this).attr("tbl"),
         api = new restAPI();
      /* - - */
      api.getTableInfo(tbl, function(jarr, tbl) {
            submenuNav.createTable(jarr, tbl);
         });
      /* - - */
      api.getClientCircuits(function(jarr) {
            submenuNav.createSelectorListItem(jarr
               , dbTableHtml.getCltCircuitSelectorItem);
         });
      /* - - */
   }

   to_delete_settingsClientSpaceCircuitsClick(__this) {
      /* - - */
      gui.loadDataBlockXml("databaseEditorFrame");
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

};
