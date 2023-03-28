
const gpio = {

   init() {
      /* -- */
      const sel = ".gpio-channel:not(.disable)";
      const coll = document.querySelectorAll(sel);
      let conf = null;
      /* -- */
      for (let e of coll)
         e.addEventListener("click", gpio.onChannelClick);
      /* -- */
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
