var count = 0;
var sentinel = document.querySelector("#dashboard-browse-program-sentinel");
var template = $("#dashboard-browse-program-template")[0];
var body = $("#dashboard-browse-programs")[0];

function loadItems() {
  response = get_programs(count, query, orderby);
  response
    .then((response) => response.json())
    .then((data) => {
      if (data.length == 0 && count == 0) {
        sentinel.css;
        sentinel.innerHTML = "No programs matched your search";
      } else if (data.length == 0 && count > 0) {
        sentinel.innerHTML = "No more programs";
      } else {
        for (var i = 0; i < data.length; i++) {
          let template_clone = template.content.cloneNode(true);
          template_clone.querySelector(
            "#dashboard-browse-program-card-title"
          ).innerHTML = `${data[i][1]}`;
          template_clone.querySelector(
            "#dashboard-browse-program-card-user"
          ).innerHTML = `by ${data[i][3]}`;

          if (data[i][2] == 1) {
            template_clone.querySelector(
              "#dashboard-browse-program-card-likes"
            ).innerHTML = `${data[i][2]} Like`;
          } else {
            template_clone.querySelector(
              "#dashboard-browse-program-card-likes"
            ).innerHTML = `${data[i][2]} Likes`;
          }
          template_clone.querySelector(
            "#dashboard-browse-program-card-user"
          ).href = `/account/${data[i][3]}`;

          template_clone.querySelector(
            "#dashboard-browse-program-card-more"
          ).href = `/program/${data[i][0]}`;

          body.appendChild(template_clone);
          count += 1;
        }
        if (data.length < 6) {
          sentinel.innerHTML = "No more programs";
        }
      }
    });
}

var intersectionObserver = new IntersectionObserver((entries) => {
  if (entries[0].intersectionRatio <= 0) {
    return;
  }
  loadItems();
});
intersectionObserver.observe(sentinel);

async function get_programs(count, query, orderby) {
  let response = await fetch("/load-programs", {
    method: "post",
    body: JSON.stringify({
      c: count,
      query: query,
      orderby: orderby,
    }),
  });
  return response;
}
