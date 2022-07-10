like_icon = $("#dashboard-program-actions-like-icon");

icon = $("#dashboard-program-actions-like-icon span");

like_icon.click(function () {
  var t1 = document.getElementById("dashboard-program-actions-liked");
  var t2 = document.getElementById("dashboard-program-actions-notliked");
  t1.classList.toggle("dashboard-program-actions-disabled");
  t2.classList.toggle("dashboard-program-actions-disabled");
});

copylink = $("#dashboard-program-info-settings-copylink");
copylink.click(function () {
  navigator.clipboard.writeText(window.location.href);
});

deletepost = $("#dashboard-program-info-settings-deletepost");
deletepost.click(function () {
  if (confirm("Are you sure you want to delete?") == true) {
    console.log(programid);
    responce = send_delete_request(programid, programuser);
    responce
      .then((response) => response.json())
      .then((data) => {
        if (data == true) {
          window.location.href = "/browse";
        } else {
          alert("something went wrong.");
          console.log("something went wrong");
        }
      });
  }
});
