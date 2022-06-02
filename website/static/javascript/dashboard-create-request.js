async function get_exercises(filtertext, filtertype) {
  var response = await fetch("/exercise-get", {
    method: "post",
    body: JSON.stringify({
      filtertext: filtertext,
      filtertype: filtertype,
    }),
  });
  return response.json();
}
