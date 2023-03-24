

const HTML = {

   selTime(lbl, id, cls) {
      let h, hrs = [`<select id="selHH_${id}" class="${cls}">`];
      hrs.push(`<optgroup label="Hours">`);
      for (let i = 0; i < 24; i++) {
         h = String(i).padStart(2, "0");
         hrs.push(`<option value="${h}">${h}</option>`);
      }
      hrs.push(`</optgroup><optgroup label="DayParts">`);
      hrs.push(`<option value="sunrise">Sunrise</option>`);
      hrs.push(`<option value="sunset">Sunset</option>`);
      hrs.push("</optgroup></select>");
      /* -- */
      let m, mnts = [`<select id="selMM_${id}" class="${cls}">`] 
      for (let i = 0; i <= 45; i += 15) {
         m = String(i).padStart(2, "0");
         mnts.push(`<option value="${m}">${m}</option>`);
      }
      /* -- */
      mnts.push("</select>");
      return `${lbl}&nbsp;:&nbsp;${hrs.join("")}` + 
         `&nbsp;:&nbsp;${mnts.join("")}&nbsp;&nbsp;`;
      /* -- */
   }

};
