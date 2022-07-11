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

programmeexercises = [];

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
  if (selectedexercise[0].toString() === id.toString()) {
    $(
      `#dashboard-create-modal-exercise-${id.toString()} #dashboard-create-modal-exercisesbody-title`
    )
      .css("color", "#0078e7")
      .html(name + "<span> - selected</span>");
  }
}

var modaladd = $("#dasboard-create-modal-add");

modaladd.click(function () {
  //if there is exercises selected
  if (selectedexercise.length !== 0) {
    //reset all the css styles involved
    exercisemodal.css("display", "none	");
    $(".dashboard-create-modal-exercisesbody-title").css("color", "black");
    $(".dashboard-create-modal-exercisesbody-title span").remove();

    programmeexercises.push(selectedexercise);

    exerciseformatpage();
    //reset form inputs and selected exercise
    selectedexercise = [];
    modalsearchselect.val("Type");
    modalsearchtext.val("");
  }
});

var create_form_body = $("#dashboard-create-form-exercises");

function exerciseformatpage() {
  //clear all the elemetns from create
  create_form_body
    .contents(":not(template,#dashboard-create-showmodal)")
    .remove();

  $("#dashboard-create-showmodal").css("display", "none");

  //if there are exercises do this
  if (programmeexercises.length > 0) {
    create_form_body.addClass("create-form-display-grid");

    for (var i = 0; i < programmeexercises.length; i++) {
      var exercise_form_template = $("#dashboard-create-form-template")[0];
      var exercise_clone_form = exercise_form_template.content.cloneNode(true);

      exercise_clone_form.querySelector(
        "#dashboard-create-form-exercisesbody-title"
      ).innerHTML = programmeexercises[i][1].toString();

      exercise_clone_form.querySelector(
        "#dashboard-create-form-exercisesbody-subtitle "
      ).innerHTML = programmeexercises[i][2];

      exercise_clone_form
        .querySelector("#dashboard-create-form-exercisesbody")
        .setAttribute(
          "id",
          "dashboard-create-form-exercise-" + programmeexercises[i][0]
        );

      exercise_clone_form
        .querySelector("#dashboard-create-form-removeexercise")
        .setAttribute("id", `dashboard-create-form-removeexercise-${i}`);

      //add themplate to the dom
      create_form_body[0].appendChild(exercise_clone_form);

      //add a on click function for each remove exercise to remove exercises
      $(`#dashboard-create-form-removeexercise-${i}`).on("click", function () {
        var id = $(this).attr("id");
        //get int from id
        var i = id.replace(/[^\d.]/g, ""); //found on https://stackoverflow.com/questions/10780087/getting-integer-value-from-a-string-using-javascript-jquery

        //if it is the last exercise clear the selected exercises else remove the exercise with the id from the list.
        if (programmeexercises.length <= 1) {
          programmeexercises = [];
        } else {
          programmeexercises.splice(i, 1);
        }

        //format page
        exerciseformatpage();
      });
    }

    //add themplate to the dom

    create_form_body[0].appendChild(
      $("#dashboard-create-form-plustemplate")[0].content.cloneNode(true)
    );
  }
  //if there are no exercises do this
  else if (programmeexercises.length == 0) {
    create_form_body.removeClass("create-form-display-grid");
    $("#dashboard-create-showmodal").css("display", "flex");
  }
}

$("#dashboard-create-form-submit").click(function () {
  playlistname = $("#dashboard-create-form-text-name").val();
  description = $("#dashboard-create-form-text-description").val();
  exercises = programmeexercises;
  responce = send_exercise_program(playlistname, description, exercises);

  responce
    .then((response) => response.json())
    .then((data) => {
      if (data[0] == true) {
        window.location.href = "/program/" + data[1];
      }
      if (data[0] == false) {
        $("#dashbord_create_error").css("display", "block");
        $("#dashboard-create-errormessage").text(data[1]);
      }
    });
});
