function showPopup(message) {
  // Create popup container
  var popup = document.createElement("div");
  popup.classList.add("popup-notification");

  // Add close button
  var closeButton = document.createElement("button");
  closeButton.innerHTML = "&times;";
  closeButton.classList.add("close-btn");
  closeButton.onclick = function () {
    popup.remove();
  };

  // Append message and close button to popup
  popup.innerHTML = message;
  popup.appendChild(closeButton);

  // Add popup to the body
  document.body.appendChild(popup);
}
