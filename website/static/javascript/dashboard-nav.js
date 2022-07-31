//add blue highlight on nav element when on page
const activePage = window.location.pathname;

if (activePage === "/dashboard") {
  document
    .getElementById("dashboard-nav-home-icn")
    .classList.add("dashboard-nav-navelement-active");

  console.log(activePage);
}
if (activePage === "/browse") {
  document
    .getElementById("dashboard-nav-browse-icn")
    .classList.add("dashboard-nav-navelement-active");

  console.log(activePage);
}

if (activePage === `/account/${username}`) {
  document
    .getElementById("dashboard-nav-account-icn")
    .classList.add("dashboard-nav-navelement-active");

  console.log(activePage);
}

if (activePage === "/create") {
  document
    .getElementById("dashboard-nav-create-icn")
    .classList.add("dashboard-nav-navelement-active");

  console.log(activePage);
}

//styles for hamburger menu to toggle nav
var hamburger = $("#dashboard-nav-hamburger");
var nav = $("#dashboard-navleft");

hamburger.click(function () {
  nav[0].classList.toggle("active");
  hamburger[0].classList.toggle("active");
});

$(window).resize(function () {
  nav[0].classList.remove("active");
  hamburger[0].classList.remove("active");
});
