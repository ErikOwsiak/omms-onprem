
class orgNavigator {

   static ElecRoom = "electricalroom";
   static __this__ = null;
   static __orgjarr__ = null;
   static __lastfetch__ = null;
   static __elecroomclicked__ = null;

   constructor() {
      this.jsonArr = null;
      console.log("orgNavigator:c-tor");  
   }

   init() {
      orgNavigator.__this__ = this;
      this.loadOrgData();
   }

   loadOrgData() {
      let api = new restAPI();
      api.getOrg(this.__loadOrgData__);
   }

   __loadOrgData__(jarr) {
      /* - - - - */
      if (jarr.length == 0)
         throw "NoOrgNavDataFound";
      /* - - - - */
      orgNavigator.__orgjarr__ = jarr;
      orgNavigator.__lastfetch__ = Date.now();
      /* - - - - */
      let root = orgNavigator.__this__.findEntity(1, 0);
      /* render root */
      let buff = `<div class="et_${root.entity_type}">${root.entity_desc}</div>`;
      $("#orgNavHead").html(buff);
      let subarr = orgNavigator.__this__.findEntities("*", root.entity_dbid);
      /* render business root */
      let targetSelector = "#orgNavBody", 
         clickSelector = "div.et_geoloc div.et_head"; 
      orgNavigator.__this__.renderClickable(subarr, targetSelector
         , clickSelector, orgNavigator.__this__.geoLocOnClick);
      /* - - */
   }

   findEntity(dbid, pdbid) {
      return orgNavigator.__orgjarr__.find(e => (parseInt(e.entity_dbid) == dbid) 
         && (parseInt(e.entity_pdbid) == pdbid));
   }

   findEntities(dbid, pdbid) {
      let arrOut = orgNavigator.__orgjarr__.filter(e => {
            let dbidOK = (dbid == "*") ? true : (e.entity_dbid == dbid),
               pdbidOK = (pdbid == "*") ? true : (e.entity_pdbid == pdbid);
            return (dbidOK && pdbidOK);
         });
      return arrOut;
   }

   /* (subarr, clickSelector, __this.geoLocClicked) */
   renderClickable(arr, targetSelector, clickSelector, onItemClickCall) {
      /* - - */
      let oneachElmt = function(elmt) {
            let eroom = "";
            if (elmt.entity_type == orgNavigator.ElecRoom)
               eroom = `<xb>${elmt.entag}</xb>&nbsp;&nbsp;`;
            let etdesc = `${eroom}${elmt.entity_desc}`;
            let buff = `<div dbid="${elmt.entity_dbid}" pdbid="${elmt.entity_pdbid}"` + 
               ` class="et_${elmt.entity_type}"><div class="et_head"` +
               ` entag="${elmt.entag}">${etdesc}</div>` + 
               `<div class="et-clicked-box"></div></div>`;
            $(targetSelector).append(buff);  
         };
      /* - - */
      arr.forEach(oneachElmt);
      $(clickSelector).off().on("click", onItemClickCall);
   }

   geoLocOnClick() {
      orgNavigator.__this__.closeGeoLocs();
      /* - - */
      let dbid = $(this).parent().attr("dbid"),
         arr = orgNavigator.__this__.findEntities("*", dbid);
      console.log(arr);
      /* load buildings */
      let targetSelector = `div[dbid="${dbid}"].et_geoloc > div.et-clicked-box`,
         clickSelector = "div.et_building div.et_head";
      /* - - */
      orgNavigator.__this__.renderClickable(arr, targetSelector
         , clickSelector, orgNavigator.__this__.buildingOnClick);
   }

   buildingOnClick() {
      orgNavigator.__this__.closeBuildings();
      /* - - */
      let dbid = $(this).parent().attr("dbid"),
         arr = orgNavigator.__this__.findEntities("*", dbid);
      console.log(arr);
      let targetSelector = `div[dbid="${dbid}"].et_building > div.et-clicked-box`,
         clickSelector = "div.et_electricalroom div.et_head";
         orgNavigator.__this__.renderClickable(arr, targetSelector
         , clickSelector, orgNavigator.__this__.elecRoomOnClick);
   }

   elecRoomOnClick() {
      /* close all open elec rooms */
      orgNavigator.__this__.closeElecRooms();
      /* this is a div here */
      orgNavigator.__this__.elecRoomClicked = this;
      let etag = $(orgNavigator.__this__.elecRoomClicked).attr("entag");
      /* - - */
      let api = new restAPI();
      api.getElcRoomMeters(etag, 
         orgNavigator.__this__.__elcRoomClick__);   
   }

   __elcRoomClick__(jobj) {
      let __this = orgNavigator.__this__, 
         eroom = __this.elecRoomClicked,
         entag = $(__this.elecRoomClicked).attr("entag"), 
         e = null, buff = "", jbuff = "";
      $(eroom).next().html("");
      /* for each */
      for (let i in jobj) {
         e = jobj[i];
         jbuff = JSON.stringify(e);
         buff = `<div entag="${entag}" dbid="${e.meter_dbid}" ctag="${e.circuit_tag}"` + 
            ` title="no data found" class="meter_button_dim">${e.circuit_tag}` + 
            `<jsonbuff>${jbuff}</jsonbuff></div>`;
         /* - - */
         $(eroom).next().append(buff);
      }
      /* -- add clicks -- */
      __this.enableActiveMeters();
   }

   enableActiveMeters() {
      let api = new restAPI();
      let entag = $(this.elecRoomClicked).attr("entag");
      /* - - */
      api.getElcRoomMetersActive(entag, (jarr) => {
            gui.activateMeters(entag, jarr);
         });
   }

   closeGeoLocs() {
      let selector = "div.et_geoloc div.et-clicked-box";
      $(selector).html("");
   }

   closeBuildings() {
      let selector = "div.et_building div.et-clicked-box";
      $(selector).html("");
   }

   closeElecRooms() {
      let selector = "div.et_electricalroom div.et-clicked-box";
      $(selector).html("");
   }

};
