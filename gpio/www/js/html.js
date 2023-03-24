

const HTML = {

   selTime(lbl, id, cls) {
      let h, hrs = [`<select id="selHH_${id}" class="${cls}">`];
      for (let i = 0; i < 24; i++) {
         h = String(i).padStart(2, "0");
         hrs.push(`<option value="${h}">${h}</option>`);
      }
      hrs.push("</select>");
      let mnts = [`<select id="selMM_${id}" class="${cls}">`] 
      for (let i = 0; i <= 45; i += 15)
         mnts.push(`<option value="${i}">${i}</option>`);
      /* -- */
      mnts.push("</select>");
      return `${lbl}&nbsp;:&nbsp;${hrs.join("")}` + 
         `&nbsp;:&nbsp;${mnts.join("")}&nbsp;&nbsp;`;
      /* -- */
   }

};
