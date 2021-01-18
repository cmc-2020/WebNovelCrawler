// Inspired by https://github.com/sahil-rajput/Candice-YourPersonalChatBot 

function addBotHtml(data) {
    // diplay bot message and scroll into view
    var botHtml = '<p class="botText"><span>' + data + "</span></p>";
    $("#chatbox").append(botHtml);
    document
        .getElementById("userInput")
        .scrollIntoView({ block: "start", behavior: "smooth" });
}

function getBotResponse() {
    var rawText = $("#textInput").val();
    
    // if the input string is not just whitespace
    if (rawText.trim()) {
      // display user message
      var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
      
      // delete user message from input field
      $("#textInput").val("");
      $("#chatbox").append(userHtml);

      // scroll into view
      document
          .getElementById("userInput")
          .scrollIntoView({ block: "start", behavior: "smooth" });

      // send the message to the server, pass the response to addBotHtml()
      $.get("/get", { msg: rawText }).done(addBotHtml);
      
      // magic command triggers clearing of history
      if (rawText == "!clear") {
        $("#chatbox").empty();
        $("#textInput").val("");
      }
    }
}

// trigger function when Enter key is pressed
$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        getBotResponse();
    }
});
