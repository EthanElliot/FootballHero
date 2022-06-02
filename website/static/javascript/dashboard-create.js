var showmodal = $("#dashboard-create-showmodal");
var exercisemodal = $("#dashboard-create-exercise-modal");
var hidemodal = $("#dasboard-create-modal-close");

$(showmodal).on("click", function () {
  exercisemodal.css("display", "inline	");
});

$(hidemodal).on("click", function () {
  exercisemodal.css("display", "none	");
});

var modalsearch = $("#dashboard-create-modal-search");
var modalsearchselect = $("#dashboard-create-modal-select");
var modalsearchtext = $("#dashboard-create-modal-text");

modalsearch.click(function () {
  var selectval = modalsearchselect.val();
  var textval = modalsearchtext.val();

  if (selectval === "Type") {
    selectval = "";
  }

  var data = get_exercises(textval, selectval).then((responce) =>
    console.log(responce)
  );
});
