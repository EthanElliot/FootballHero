var showmodal = $("#dashboard-create-showmodal");
var exercisemodal = $("#dashboard-create-exercise-modal");
var hidemodal = $("#dasboard-create-modal-close");

$(showmodal).on("click", function () {
  exercisemodal.css("display", "inline	");
});

$(hidemodal).on("click", function () {
  exercisemodal.css("display", "none	");
});

//modal form inputs
var modalsearch = $("#dashboard-create-modal-search");
var modalsearchselect = $("#dashboard-create-modal-select");
var modalsearchtext = $("#dashboard-create-modal-text");

//modal exercise body
var modalbody = $("#dashboard-create-modal-exercise");

//modal loader
var modalloader = $("#dashboard-create-modal-loader");

//modal message
var modalmessage = $("#dashboard-create-modal-message");

//modal template
var modaltemplate = $("#dashboard-create-modal-template")[0];

selectedexercise = [];

modalsearch.click(function () {
  // remove all elements from the div
  modalbody
    .contents(
      ":not(template,#dashboard-create-modal-loader,#dashboard-create-modal-message)"
    )
    .remove();
  //add class to center all elements in the div
  modalbody.addClass("dashboard-create-modal-exercise-center");

  // hide text but show the loader
  modalmessage.css("display", "none");
  modalloader.css("display", "block");

  //get the filter values
  var selectval = modalsearchselect.val();
  var textval = modalsearchtext.val();

  //type should be = '' if no type is selected
  if (selectval === "Type") {
    selectval = "";
  }

  //send a post request for the data
  get_exercises(textval, selectval).then((responce) => {
    //have selected exercises added to the frount of the list
    if (selectedexercise.length !== 0) {
      for (var i = 0; i < responce.length; i++) {
        if (responce[i][0] === selectedexercise[0]) {
          responce.splice(i, 1);
        }
      }
      responce.unshift(selectedexercise);
    }

    //make the loader invisable as we have the responce
    modalloader.css("display", "none");

    if (responce.length === 0) {
      modalmessage.css("display", "block");
    } else {
      modalbody.removeClass("dashboard-create-modal-exercise-center");
      for (var i = 0; i < responce.length; i++) {
        //clone the html template
        var exercise_clone = modaltemplate.content.cloneNode(true);

        exercise_clone.querySelector(
          "#dashboard-create-modal-exercisesbody-title"
        ).innerHTML = responce[i][1];

        exercise_clone.querySelector(
          "#dashboard-create-modal-exercisesbody-subtitle "
        ).innerHTML = responce[i][2];

        exercise_clone
          .querySelector("#dashboard-create-modal-exercisesbody")
          .setAttribute(
            "id",
            "dashboard-create-modal-exercise-" + responce[i][0]
          );
        exercise_clone
          .querySelector(`#dashboard-create-modal-exercise-${responce[i][0]}`)
          .setAttribute(
            "onclick",
            `on_exerciseclick(${responce[i][0]},'${responce[i][1]}','${responce[i][2]}')`
          );

        //add themplate to the dom
        modalbody[0].appendChild(exercise_clone);
      }
    }
    if (selectedexercise.length !== 0) {
      $(
        `#dashboard-create-modal-exercise-${selectedexercise[0]} #dashboard-create-modal-exercisesbody-title`
      )
        .css("color", "#0078e7")
        .html(selectedexercise[1] + "<span> - selected</span>");
    }
  });
});

function on_exerciseclick(id, name, type) {
  //add the selected exersice to a selected list
  selectedexercise = [];
  selectedexercise = [id, name, type];
  //reset styles on the exercise titles
  $(".dashboard-create-modal-exercisesbody-title").css("color", "black");
  $(".dashboard-create-modal-exercisesbody-title span").remove();

  // add styles
  console.log(selectedexercise[0]);
  console.log(id);
  if (selectedexercise[0].toString() === id.toString()) {
    $(
      `#dashboard-create-modal-exercise-${id.toString()} #dashboard-create-modal-exercisesbody-title`
    )
      .css("color", "#0078e7")
      .html(name + "<span> - selected</span>");
  }
}
