

const HTML = {

   selTimeHH() {
      let sl, h, hrs = [];
      hrs.push(`<optgroup label="DayParts">`);
      hrs.push(`<option value="sunrise">Sunrise</option>`);
      hrs.push(`<option value="sunset">Sunset</option>`);
      hrs.push(`</optgroup><optgroup label="Hours">`);
      /* -- */
      for (let i = 0; i < 24; i++) {
         sl = (i == 0) ? " selected" : "";
         h = String(i).padStart(2, "0");
         hrs.push(`<option value="${h}"${sl}>${h}</option>`);
      }
      /* -- */
      hrs.push(`</optgroup>`);
      return hrs.join("");
      /* -- */
   },

   selTimeMM(min, max, step, posprfx = "") {
      let sl, m, mnts = [];
      for (let i = min; i <= max; i += step) {
         sl = (i == 0) ? " selected" : "";
         m = String(i).padStart(2, "0");
         m = (i > 0) ? `+${m}` : m;
         mnts.push(`<option value="${m}"${sl}>${m}</option>`);
      }
      return mnts.join("");   
   }

};
