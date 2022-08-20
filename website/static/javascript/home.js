//add drop shadow on scroll
window.addEventListener("scroll", (e) => {
  const nav = $("#home-navigation");
  if (window.pageYOffset > 0) {
    nav.css("box-shadow", " 0px 1px 2px 0px rgba(60, 64, 67, 0.3)");
  } else {
    nav.css("box-shadow", " none");
  }
});

//styles for hamburger menu to toggle nav
var hamburger = $("#home-nav-hamburger");
var nav = $("#home-nav-butons");

hamburger.click(function () {
  nav[0].classList.toggle("active");
  hamburger[0].classList.toggle("active");
});

$(window).resize(function () {
  nav[0].classList.remove("active");
  hamburger[0].classList.remove("active");
});
