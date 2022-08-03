var accountmodal = $("#dashboard-account-modal");

var editinfo = $("#dashboard-account-info-settings-editinfo");
var deleteaccount = $("#dashboard-account-info-settings-deleteaccount");

var editinfo_modal = $("#dashboard-account-modal-editinfo");
var deleteaccount_modal = $("#dashboard-account-modal-deleteaccount");

var editinfo_modal_close = $("#dashboard-account-modal-editinfo-close");
var deleteaccount_modal_close = $(
  "#dashboard-account-modal-deleteaccount-close"
);

editinfo.on("click", function () {
  accountmodal.css("display", "block");
  editinfo_modal.css("display", "block");
});

deleteaccount.on("click", function () {
  accountmodal.css("display", "block");
  deleteaccount_modal.css("display", "block");
});

editinfo_modal_close.on("click", function () {
  accountmodal.css("display", "none");
  editinfo_modal.css("display", "none");
});
deleteaccount_modal_close.on("click", function () {
  accountmodal.css("display", "none");
  deleteaccount_modal.css("display", "none");
});

$("#dashboard-account-modal-form-error-delete-close").on("click", function () {
  $("#dashboard-account-modal-form-error-delete-wrapper").css(
    "display",
    "none"
  );
});

$("#dashboard-account-modal-form-error-edit-close").on("click", function () {
  $("#dashboard-account-modal-form-error-edit-wrapper").css("display", "none");
});

$("#dashboard-account-modal-form-delete").on("click", function () {
  responce = send_delete_account(
    username,
    $("#dashboard-account-modal-form-password-delete").val()
  );

  responce
    .then((response) => response.json())
    .then((data) => {
      if (data[0] == true) {
        location.replace("/");
      }
      if (data[0] == false) {
        $("#dashboard-account-modal-form-error-delete-message").html(data[1]);

        $("#dashboard-account-modal-form-error-delete-wrapper").css(
          "display",
          "flex"
        );
      }
    });
});

$("#dashboard-account-modal-form-edit").on("click", function () {
  console.log("yes");
  updateinfo = {
    username: $("#dashboard-account-modal-form-username").val(),
  };

  responce = send_edit_account(
    username,
    updateinfo,
    $("#dashboard-account-modal-form-password-edit").val()
  );
  responce
    .then((response) => response.json())
    .then((data) => {
      if (data[0] == true) {
        location.replace(`/account/${data[1]}`);
      }
      if (data[0] == false) {
        $("#dashboard-account-modal-form-error-edit-message").html(data[1]);

        $("#dashboard-account-modal-form-error-edit-wrapper").css(
          "display",
          "flex"
        );
      }
    });
});
