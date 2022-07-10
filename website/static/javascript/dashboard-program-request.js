async function send_delete_request(id, username) {
  let response = await fetch("/delete-program", {
    method: "post",
    body: JSON.stringify({
      id: id,
      username: username,
    }),
  });
  return response;
}
