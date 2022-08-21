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
