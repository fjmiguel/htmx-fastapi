'use strict';

//WIP
/* const editItemTemplate =
  `<li id="item-{{id}}">
    <form
      hx-put="http://localhost:8080/items/{{id}}"
      hx-target="#item-{{id}}"
      hx-swap="outerHTML"
    >
      <input type="text" name="name" value="{{name}}">

      <button type="submit">Save</button>

      <button
        hx-get="http://localhost:8080/items"
        hx-target="#item-{{id}}"
        hx-swap="outerHTML">
      Cancel
      </button>
    </form>
  </li>`; */

function renderItem(item) {
  if (item?.detail) {
    alert(item.detail);
    return '';
  }

  if (!item?.id || !item.name) {
    console.log('Unknown error');
    return '';
  }

  const itemTemplate =
    `<li id="item-{{id}}">
      <span>{{name}}</span>

      <button
      class="edit-button"
      hx-get="http://localhost:8080/items/{{id}}/edit"
      hx-target="#item-{{id}}"
      hx-swap="outerHTML">
      Edit
      </button>

      <button
      class="delete-button"
      hx-delete="http://localhost:8080/items/{{id}}"
      hx-target="#item-{{id}}"
      hx-swap="outerHTML">
      Delete
      </button>
    </li>`;


  return itemTemplate
    .replace(/{{id}}/g, item.id)
    .replace(/{{name}}/g, item.name);
}

function renderItems(items) {
  if (items.length === 0) {
    return;
  }

  let renderedItems = '';

  items.forEach(
    item => {
      renderedItems += renderItem(item).trim()
    }
  );

  return renderedItems;
}

function clearInput(form) {
  const input = form.querySelector('input[name="name"]');
  input.value = '';
  input.focus();
}
