
const gpio = {

   init() {
      /* -- */
      let conf = null;
      const sel = ".gpio-channel:not(.disable)";
      const coll = document.querySelectorAll(sel);
      /* -- */
      for (let e of coll)
         e.addEventListener("click", gpio.onChannelClick);
      /* -- */
      const holidays = [new Holiday(1, 1, "New Year"), new Holiday(1, 6, "Three Kings")
         , new Holiday(5, 1, "Labor Day"), new Holiday(5, 3, "Constitution Day")
         , new Holiday(8, 15, "Army Day"), new Holiday(11, 1, "All Saints' Day")
         , new Holiday(11, 11, "Independence Day"), new Holiday(12, 25, "Xmas")
         , new Holiday(12, 26, "Xmas 2nd")]
   },

   onChannelClick() {
      /* -- */
      const devid = this.getAttribute("devid");
      const ch = this.getAttribute("ch");
      const sel = `${devid}Conf`;
      /* -- */
      const coll0 = document.getElementsByClassName("channel-conf");
      for (let e of coll0) {
         e.style.display = "none";
         e.innerHTML = "";
      }
      /* -- */
      const coll1 = document.getElementsByClassName("gpio-channel");
      for (let e of coll1) {
         e.style.backgroundColor = "";
         e.style.border = "1px solid gray";
      }
      /* -- */
      this.style.backgroundColor = "rgba(211, 211, 211, 0.32)";
      this.style.border = "2px solid darkblue";
      const elm = document.getElementById(sel)
      elm.style.display = "block";
      elm.style.backgroundColor = "rgba(211, 211, 211, 0.2)";
      elm.innerHTML = gpio.getNewConfForm();
      setTimeout(() => {
            const div0 = document.getElementById("channelInfo");
            div0.innerText = `${devid} : ${ch}`;
            console.log(div0.innerHTML);
         }, 100);
      /* -- */
      this.conf = new gpioConf(devid, ch);
      this.conf.init();
      /* -- */
   },

   getNewConfForm() {
      const sel = "#formIsland #_chConfForm";
      const e = document.querySelector(sel);
      return e.outerHTML;   
   }

};


/* -- -- */
document.addEventListener("DOMContentLoaded"
   , gpio.init);
/* -- -- */
