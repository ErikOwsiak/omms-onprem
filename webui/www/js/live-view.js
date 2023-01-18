
const liveView = {

   restapi: null,

   init() {
      liveView.restapi = new restAPI();
      liveView.restapi.getClients(liveView.onGetClients);
   },

   run() {

   },

   onGetClients(json) {
      console.log(json);
   }

};
