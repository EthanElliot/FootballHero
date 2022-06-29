async function get_exercises(filtertext, filtertype) {
  let response = await fetch("/exercise-get", {
    method: "post",
    body: JSON.stringify({
      filtertext: filtertext,
      filtertype: filtertype,
    }),
  });
  return response.json();
}

async function send_exercise_program(name, description, exercises) {
  let response = await fetch("/create-program", {
    method: "post",
    body: JSON.stringify({
      name: name,
      description: description,
      exercises: exercises,
    }),
  });
  if (response) {
    return response
  }
}