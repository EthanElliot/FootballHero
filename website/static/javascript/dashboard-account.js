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

$("#dashboard-account-modal-form-error-close").on("click", function () {
  $("#dashboard-account-modal-form-error-wrapper").css("display", "none");
});

$("#dashboard-account-modal-form-delete").on("click", function () {
  responce = send_delete_account(
    username,
    $("#dashboard-account-modal-form-password").val()
  );

  responce
    .then((response) => response.json())
    .then((data) => {
      if (data[0] == true) {
        location.replace("/");
      }
      if (data[0] == false) {
        $("#dashboard-account-modal-form-error-message").html(data[1]);

        $("#dashboard-account-modal-form-error-wrapper").css("display", "flex");
      }
    });
});
