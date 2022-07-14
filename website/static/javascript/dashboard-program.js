like_icon = $("#dashboard-program-actions-like-icon");
like_text = $("#dashboard-program-actions-like-text");

icon = $("#dashboard-program-actions-like-icon span");

like_icon.click(function () {
  responce = send_like_request(programid);
  responce
    .then((response) => response.json())
    .then((data) => {
      if (data.liked_by_user == true) {
        if (data.likes == 1) {
          like_text.text("Liked by you");
        } else if (data.likes == 2) {
          like_text.text(`liked by you and 1 other`);
        } else if (data.likes > 1) {
          like_text.text(`liked by you and ${data.likes - 1} others`);
        }
      } else {
        if (data.likes == 0) {
          like_text.text("Liked by 0 users");
        } else if (data.likes == 1) {
          like_text.text(`liked by 1 user`);
        } else if (data.likes > 0) {
          like_text.text(`liked by ${data.likes} users`);
        }
      }
      var t1 = document.getElementById("dashboard-program-actions-liked");
      var t2 = document.getElementById("dashboard-program-actions-notliked");
      t1.classList.toggle("dashboard-program-actions-disabled");
      t2.classList.toggle("dashboard-program-actions-disabled");
    });
});

copylink = $("#dashboard-program-info-settings-copylink");
copylink.click(function () {
  navigator.clipboard.writeText(window.location.href);
});

deletepost = $("#dashboard-program-info-settings-deletepost");
deletepost.click(function () {
  if (confirm("Are you sure you want to delete?") == true) {
    responce = send_delete_request(programid, programuser);
    responce
      .then((response) => response.json())
      .then((data) => {
        if (data == true) {
          window.location.href = "/browse";
        } else {
          alert("something went wrong.");
        }
      });
  }
});
