const deleteButton = document.querySelector("#deleteAccount");
const deleteButtonReal = document.querySelector("#deleteAccountReal");
const userInfo = document.querySelector("#userInfo");

const emojiButton = document.querySelector("#emojiButton");
const emojiBox = document.querySelector("#emojiBox");

// User Account Delete Button
deleteButton.addEventListener("click", () => {
  input = prompt("Please enter your current username to confirm deletion.");
  if (input === userInfo.textContent) {
    deleteButtonReal.style.display = "block";
    deleteButton.style.display = "none";
  } else {
    alert("Information is Incorrect.");
    deleteButtonReal.style.display = "none";
  }
});

// Emojis
emojiButton.addEventListener("click", () => {
  console.log("!");
  if (emojiBox.style.display === "none") {
    emojiBox.style.display = "grid";
  } else {
    emojiBox.style.display = "none";
  }
});

/*
<button id="emojiButton">Emoji</button>
<div id="emojiBox">
  <button class="emoji">😊</button>
  <button class="emoji">😂</button>
  <button class="emoji">😭</button>
  <button class="emoji">😒</button>
  <button class="emoji">👌</button>
  <button class="emoji">👍</button>
  <button class="emoji">❤️</button>
  <button class="emoji">😎</button>
  <button class="emoji">🎶</button>
  <button class="emoji">🤔</button>
  <button class="emoji">😫</button>
  <button class="emoji">😡</button>
</div>
*/
