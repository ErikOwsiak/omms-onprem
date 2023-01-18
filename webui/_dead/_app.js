
function include(fl, ctype, tagname) {
   var tag = document.createElement(tagname);
   tag.src = `js/${fl}`;
   tag.type = ctype;
   tag.defer = true;
   document.getElementsByTagName("head").item(0).appendChild(tag);
};

const app_js_files = ["reports/histogram.js", "reports/kwhrs-report.js", "db-table.js"];
app_js_files.forEach(f => include(f, "text/javascript", "script"));
