    function processFeedback(scenario_id) {
      $("#scenario_name").text(feedback_data.name);
      $("#scenario_description").text(feedback_data.description);
      $("#scenario_result").html("<strong>" + feedback_data.result.text + "</strong>");

      if (!feedback_data.result.bool) {
        $("#scenario_feedback").text(feedback_data.feedback.text);
      }

      var command_line = "C:\\Magshimim> program.exe";
      for (var i = 0; i < feedback_data.args.length; i++) {
        command_line += " " + feedback_data.args[i];
      }
      $("#scenario_log").append("<li>" + command_line + "<li>")

      comments = [];

      for (var i = 0; i < feedback_data.log.quotes.length; i++) {
        var line = $('<li></li>');
        line.text(feedback_data.log.quotes[i].value);

        if (feedback_data.log.quotes[i].type.en == "input" || feedback_data.log.quotes[i].type.en == "output") {
          line.addClass("commentable-section");
          line.attr("data-section-id", i.toString());

          comments.push({
            "sectionId": i.toString(),
            "comments": [
              {
                "id": i.toString(),
                "authorAvatarUrl": COMMENTS_IMAGES[feedback_data.log.quotes[i].type.en],
                "authorName": feedback_data.log.quotes[i].type.he,
                "comment": feedback_data.log.quotes[i].name
              }
            ]
          });
      }

      $("#scenario_log").append(line);
    }

      if (!feedback_data.result.bool) {
        var line = $('<li></li>');
        line.html("<br>")
        line.addClass("commentable-section");
        line.attr("data-section-id", "feedback")

        comments.push({
          "sectionId": "feedback",
          "comments": [
            {
              "id": "feedback",
              "authorAvatarUrl": COMMENTS_IMAGES[feedback_data.result.bool.toString() + "_"],
              "authorName": feedback_data.result.text,
              "comment": feedback_data.feedback
            }
          ]
        });

        $("#scenario_log").append(line);

      }

    var currentUser = {
      "id": 4,
      "avatarUrl": "support/images/user.png",
      "authorUrl": "http://google.com/",
      "name": "You"
    };

  var SideComments = require('side-comments');
  window.sideComments = new SideComments('#commentable-container', currentUser, comments);
}
