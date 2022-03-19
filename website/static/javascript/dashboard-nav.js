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

if (activePage === "/account") {
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
