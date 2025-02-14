function getCookie(name) {
  const cookies = document.cookie.split("; ");
  for (const cookie of cookies) {
    const [key, value] = cookie.split("=");
    if (key === name) {
      return decodeURIComponent(value);
    }
  }
  return null;
}

document.addEventListener("DOMContentLoaded", () => {
  const loadingText = document.getElementById("loadingText");
  const inputField = document.querySelector(".inputField");

  if (getCookie("token") === null) {
    loadingText.innerHTML =
      "<a href='/login'><img src='/static/img/sign-in-with-x.svg' width='50%' alt='Xでサインイン' style='background-color: #000; padding: 10px; padding-left: 20px; padding-right: 20px; border-radius: 10px;'></img></a>";
    return;
  }

  loadingText.style.display = "none";
  inputField.style = "";

  document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    if (
      document.getElementById("submitButton").classList.contains("is-loading")
    ) {
      return;
    }

    if (document.getElementById("reasonTextArea").value.length < 5) {
      alert("好きな理由は最低でも5文字は書いてください");
      return;
    }

    document.getElementById("submitButton").classList.add("is-loading");

    const userName = document.getElementById("userNameInput").value;
    const response = await fetch(`/api/x/lookup/${userName}`);

    if (response.status != 200) {
      alert("ユーザーが存在しません。");
      document.getElementById("submitButton").classList.remove("is-loading");
      return;
    }

    const userData = await response.json();

    document
      .getElementById("warningIcon")
      .setAttribute("src", userData.iconUrl);

    document.getElementById(
      "warningMessage"
    ).textContent = `${userData.name} さんに投票しますか？`;

    document.getElementById("vote").setAttribute("aria-x-id", userData.id);
    document.getElementById("modal").classList.add("is-active");

    document.getElementById("submitButton").classList.remove("is-loading");
  });

  const voteButton = document.getElementById("vote");
  voteButton.addEventListener("click", async (e) => {
    const xUserId = voteButton.getAttribute("aria-x-id");
    console.log(xUserId);
    console.log(document.getElementById("reasonTextArea").value);
    const response = await fetch("/api/poll", {
      headers: {
        "content-type": "application/json",
        cookies: document.cookies,
      },
      method: "POST",
      body: JSON.stringify({
        to: xUserId,
        reason: document.getElementById("reasonTextArea").value,
      }),
    });
    if (response.status != 200) {
      const jsonData = await response.json();
      alert(jsonData.detail);
      return;
    }
    alert("投票しました。");
    window.location.href = "/";
  });
});

document.addEventListener("DOMContentLoaded", () => {
  // Functions to open and close a modal
  function openModal($el) {
    $el.classList.add("is-active");
  }

  function closeModal($el) {
    $el.classList.remove("is-active");
  }

  function closeAllModals() {
    (document.querySelectorAll(".modal") || []).forEach(($modal) => {
      closeModal($modal);
    });
  }

  // Add a click event on buttons to open a specific modal
  (document.querySelectorAll(".js-modal-trigger") || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);

    $trigger.addEventListener("click", () => {
      openModal($target);
    });
  });

  // Add a click event on various child elements to close the parent modal
  (
    document.querySelectorAll(
      ".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button"
    ) || []
  ).forEach(($close) => {
    const $target = $close.closest(".modal");

    $close.addEventListener("click", () => {
      closeModal($target);
    });
  });

  // Add a keyboard event to close all modals
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeAllModals();
    }
  });
});
