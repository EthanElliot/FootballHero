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

async function send_edit_account(username, updateinfo, password) {
  let response = await fetch("/edit-account", {
    method: "post",
    body: JSON.stringify({
      username: username,
      updateinfo: updateinfo,
      password: password,
    }),
  });
  return response;
}
