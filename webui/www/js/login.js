
var login = {

   init() {
      /* read url for msg = ??? */
      let re = /\?msg=([\w+]{2,32})/gm,
         m = re.exec(window.location.href);
      if ((m == null) || (m.length != 2))
         return;
      /* - - */
      switch(m[1].trim()) {
         case "BadLogin":
            let mbox = document.getElementById("msgBox");
            mbox.innerText = "Bad UserID or Password! Please try again."
            mbox.classList.add("msg-box-error");
            break;
         default:
            break
      }
   }

};

/* attach page loaded event */
window.addEventListener("DOMContentLoaded", login.init);
