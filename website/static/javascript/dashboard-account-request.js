async function send_delete_account(username, password) {
  let response = await fetch("/delete-account", {
    method: "post",
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  });
  return response;
}
