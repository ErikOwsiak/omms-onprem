
/*
const formData = new FormData();
const fileField = document.querySelector('input[type="file"]');

formData.append('username', 'abc123');
formData.append('avatar', fileField.files[0]);

fetch('https://example.com/profile/avatar', {
  method: 'PUT',
  body: formData
})
.then(response => response.json())
.then(result => {
  console.log('Success:', result);
})
.catch(error => {
  console.error('Error:', error);
});

    this.sessionCheckUrl = "/api/session/check";
    this.sessionLoginUrl = "/api/session/login";
    this.sessionLogoutUrl = "/api/session/logout";

*/

let sessCookie = document.cookie;
console.log(sessCookie);


var session = {

   checkUrl: "/api/session/check",
   loginUrl: "/api/session/login",
   logoutUrl: "/api/session/logout",

   check() {

   },

   login() {

   },

   logout() {

   }

};

//document.cookie = "openbms-session=44444444;SameSite=Lax;";
