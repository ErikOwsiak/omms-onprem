
class OpenGPIO {

   static gpioUrl = "10.0.0.122:8099/ogpio";
   static IFrameBuffer = `<iframe src=\"${OpenGPIO.gpioUrl}\"` +
      ` id=\"GpioIFrame\" class=\"gpio-iframe\" />`;

   constructor(divID) {
      this.divID = divID;
   }

   init() { 
      $(`#${this.divID}`).html(OpenGPIO.IFrameBuffer);
      if (SystemOverview.__this__ ) {
         console.log(SystemOverview.__this__ );
         
      } else {
         console.log("SystemOverview.__this__: false");
      }
   }

};
