const pageTitle = document.title.trim();

const deleteButton = document.querySelector("#deleteAccount");
const deleteButtonReal = document.querySelector("#deleteAccountReal");
const userInfo = document.querySelector("#userInfo");

const emojiButton = document.querySelector("#emojiButton");
const emojiBox = document.querySelector("#emojiBox");
const emoji = document.querySelectorAll(".emoji");
const bar = document.querySelector(".CommentBar");

const deleteChannelButton = document.querySelector("#deleteChannel");
const deleteChannelButtonReal = document.querySelector("#deleteChannelReal");
const channelInfo = document.querySelector("#channelInfo");

document.addEventListener("DOMContentLoaded", () => {
  if (pageTitle === "Profile") {
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
  } else if (pageTitle.startsWith("Settings")) {
    deleteChannelButton.addEventListener("click", () => {
      input = prompt("Please enter your channel name to confirm deletion.");
      if (input === channelInfo.textContent) {
        deleteChannelButtonReal.style.display = "block";
        deleteChannelButton.style.display = "none";
      } else {
        alert("Information is Incorrect.");
        deleteButtonReal.style.display = "none";
      }
    });
  } else {
    for (let i = 0; i < 36; i++) {
      emoji[i].addEventListener("click", () => {
        bar.value += emoji[i].textContent;
      });
    }
    emojiButton.addEventListener("click", () => {
      if (emojiBox.style.display == "none") {
        emojiBox.style.display = "grid";
      } else {
        emojiBox.style.display = "none";
      }
    });
  }
});
