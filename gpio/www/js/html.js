

const HTML = {

   selTime(id, cls) {
      let hrs = [`<select id="HH_${id}" class="${cls}">`];
      for (let i = 0; i < 24; i++) {
         let h = String(i).padStart(2, "0");
         hrs.push(`<option value="${h}">${h}</option>`);
      }
      hrs.push("</select>&nbsp;:&nbsp;");
      let mnts = [`<select id="MM_${id}" class="${cls}">`] 
      for (let i = 15; i <= 45; i += 15)
         mnts.push(`<option value="${i}">${i}</option>`);
      /* -- */
      mnts.push("</select>");
      return hrs.join("");
   }

};
