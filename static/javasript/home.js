//add drop shadow on scroll
window.addEventListener("scroll", (e) => {
  const nav = document.querySelector("nav");
  if (window.pageYOffset > 0) {
    nav.style.boxShadow = " 0px 1px 2px 0px rgba(60, 64, 67, 0.3)";
  } else {
    nav.style.boxShadow = "none";
  }
});
