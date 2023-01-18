
var html = {

   subMenuHead(headTite, headMsg) {
      return `<div><div class=\"submenu-col-head\">` + 
         `<div>${headTite}</div><div>${headMsg}</div></div>` + 
         `<div id="submenuColBody" class=\"submenu-col-body\"></div></div>`;
   },

   liveViewSubMenu(headTite, headMsg) {
      return html.subMenuHead(headTite, headMsg);
   },

   lblTextBox(lbl, val, disabled = true) {
      let dis = (disabled) ? "disabled" : "";
      return `<div class="read-item"><label>${lbl}:</label>` + 
         `<input type="text" value="${val}" ${dis} /></div>`;
   },

   dlOpt(obj) {
      let val = `${obj.entag} - ${obj.entity_type} - ${obj.entity_desc}`;
      return `<option entag="${obj.entag}" value="${val}">`;
   },

   kwhrsReportLine(arr) {
      if (arr == null)
         return `<div class="kwhrs-rpt-ln">no data found</dvi>`;
      /* - - */
      let [dbid, cirtag,,, sptag, kwhrs] = arr;
      kwhrs = gui.format_kwh(kwhrs);
      return `<div class="kwhrs-rpt-ln"><div>dbid:&nbsp;${dbid}</div>` + 
         `<div>circuit:&nbsp;${cirtag}</div><div>space:&nbsp;${sptag}</div>` + 
         `<div>${kwhrs}&nbsp;kWh</div></div>`;
   },

   kwhrsReportLinePerSpace(obj) {
      if (obj == null)
         return `<div class="kwhrs-rpt-ln">no data found</div>`;
      /* - - */
      kwhs = gui.format_kwh(obj.kwhs);
      return `<div class="kwhrs-rpt-ln"><div>space:&nbsp;${obj.space}</div>` + 
         `<div>circuit(s):&nbsp;${obj.ctags}</div><div>${kwhs}&nbsp;kWh</div></div>`;
   },

   kwhrsReportCltBox(clt, id, total) {
      if ([0, "0"].includes(total))
         total =  gui.format_kwh(total);
      return `<div id="${id}" class="kwhrs-rpt-clt"><div class="clt-meter-hdr">` + 
         `<div>name:&nbsp;<b>${clt.client_name}</b></div><div>tag:&nbsp;<b>${clt.client_tag}</b></div>` + 
         `<div><b>${total}</b>&nbsp;kWh</div></div><div class="clt-meter-lst"></div></div>`;
   },

   kWhPreviewTable(body) {
      let head = `<tr><th>client tag</th><th>client name</th><th>client space</th>` +
         `<th>circuit tag(s)</th><th>kWh</th></tr>`;
      /* - - */
      return `<table id="tblReportPreview" class="kwhrs-rpt-preview">` +
         `${head}${body}</table>`;
   },

   kWhPreviewTableRow(clttag, cltname, cltsp, cirtag, kwh) {
      let kwhloc = gui.format_kwh(kwh);
      return `<tr><td>${clttag}</td><td>${cltname}</td><td>${cltsp}</td>` + 
         `<td>${cirtag}</td><td>${kwhloc}</td></tr>`;
   },

   kWhPreviewBottomBar() {
      let input = `<input type="button" id="btnSave_kWhReport" value="save" />`
      return `<div class="kwh-bottom-bar-ctrl">${input}</div>`;
   },

   elecRoomButton(elmt) {
      /* - - */
      let eroom = `<xb>${elmt.entag}</xb>&nbsp;&nbsp;`,
         etdesc = `${eroom}${elmt.entity_desc}`,
         buff = `<div dbid="${elmt.entity_dbid}" pdbid="${elmt.entity_pdbid}"` + 
            ` class="et_${elmt.entity_type}"><div class="et_head">` + 
            `${etdesc}</div><div class="et-clicked-box"></div></div>`;
      /* - - */
      return buff;
   },

   ping(args) {
      /* - - */
      let [ip, edge, dts, late] = args,
         css = (late) ? "ping-late" : "ping-ontime";
      dts = dts.split(".")[0]; 
      /* - - */
      return `<div class="sys-ping ${css}"><div>EDGE:&nbsp;&nbsp;${edge}</div>` + 
         `<div>From&nbsp;IP:&nbsp;&nbsp;${ip}</div><div>@UTC:&nbsp;&nbsp;${dts}</div></div>`;
   }

}
