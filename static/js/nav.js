// (function () {
//     const toggle = document.getElementById("login-toggle");
//     const form = document.getElementById("login-form");

//     if (!toggle || !form) {
//         return;
//     }

//     toggle.addEventListener("click", function (event) {
//         event.stopPropagation();
//         const visible = form.style.display === "block";
//         form.style.display = visible ? "none" : "block";
//         form.setAttribute("aria-hidden", visible ? "true" : "false");
//     });

//     document.addEventListener("click", function (event) {
//         if (!form.contains(event.target) && event.target !== toggle) {
//             form.style.display = "none";
//             form.setAttribute("aria-hidden", "true");
//         }
//     });
// })();