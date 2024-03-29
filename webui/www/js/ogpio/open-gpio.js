
class OpenGPIO {

   static gpioUrl = "/omms/gpio?mode=iframe";
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
