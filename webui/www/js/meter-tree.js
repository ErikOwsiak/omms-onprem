
class orgXmlNavTree {

   constructor(jarr) {
      this.jsonArr = jarr;
      this.bodyHtml = {};
   }

   treeViewHolder() {
      return `<div id="meterTreeView" class="tree-view"></div>`;
   }

   loadView(keyName) {
      for (let i in this.jsonArr)
         this.bucketByKeyName(keyName, this.jsonArr[i]);
      /* attche clicks */
      $(".cls_meter").off().on("click", app.meterOnClick);
   }

   bucketByKeyName(key, item) {
      /* check key in object */
      if (item[key] == undefined)
         return;
      /* get bocket */
      let bucketID = `ID_${item.edge_name}`,
         selector = `#${bucketID}`;
      /* check if bucket exists if not create */
      if ($(selector).length == 0) {
         let bucketHtml = `<div id="${bucketID}" class="cls_${key}">` + 
            `<div class="cls_bucket_css">${item.edge_name}</div>` + 
            `<div class=""></div></div>`;
         /* - - */
         $("#submenuColBody").html(bucketHtml);
      }
      /* -- crates meter button -- */
      let dbid = item.meter_dbid, 
         htmlBuff = `<div id="DBID_${dbid}" dbid="${dbid}" class="cls_meter">` +
         `<jsonbuff>${JSON.stringify(item)}</jsonbuff>` +  
         `<div class="meter_ln cls_cir_lbl">circuit: <b>${item.circuit_tag}</b></div></div>`;
      /* append to bucket */
      $(selector).append(htmlBuff);
   }

};
