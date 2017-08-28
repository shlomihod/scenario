function processFeedback(feedbackData, scenarioId) {
      scenarioIdStr = "-" + scenarioId
      $("#scenario_name" + scenarioIdStr).text(feedbackData.name);
      $("#scenario_description" + scenarioIdStr).text(feedbackData.description);
      $("#scenario_result" + scenarioIdStr).html("<strong>" + feedbackData.result.text + "</strong>");

      if (!feedbackData.result.bool) {
        $("#scenario_feedback" + scenarioIdStr).text(feedbackData.feedback.text);
      }

      var command_line = "C:\\Magshimim> program.exe";
      for (var i = 0; i < feedbackData.args.length; i++) {
        command_line += " " + feedbackData.args[i];
      }
      $("#scenario_log" + scenarioIdStr).append("<li>" + command_line + "<li>")

      comments = [];

      for (var i = 0; i < feedbackData.log.quotes.length; i++) {
        var line = $('<li></li>');
        line.text(feedbackData.log.quotes[i].value);

        if (feedbackData.log.quotes[i].type.en == "input" || feedbackData.log.quotes[i].type.en == "output") {
          line.addClass("commentable-section");
          line.attr("data-section-id", i.toString());

          comments.push({
            "sectionId": i.toString(),
            "comments": [
              {
                "id": i.toString(),
                "authorAvatarUrl": COMMENTS_IMAGES[feedbackData.log.quotes[i].type.en],
                "authorName": feedbackData.log.quotes[i].type.he,
                "comment": feedbackData.log.quotes[i].name
              }
            ]
          });
      }

      $("#scenario_log" + scenarioIdStr).append(line);
    }

      if (!feedbackData.result.bool) {
        var line = $('<li></li>');
        line.html("<br>")
        line.addClass("commentable-section");
        line.attr("data-section-id", "feedback")

        comments.push({
          "sectionId": "feedback",
          "comments": [
            {
              "id": "feedback",
              "authorAvatarUrl": COMMENTS_IMAGES[feedbackData.result.bool.toString() + "_"],
              "authorName": feedbackData.result.text,
              "comment": feedback_data.feedback
            }
          ]
        });

        $("#scenario_log" + scenarioIdStr).append(line);

      }

    var currentUser = {
      "id": 4,
      "avatarUrl": "support/images/user.png",
      "authorUrl": "http://google.com/",
      "name": "You"
    };

  var SideComments = require('side-comments');
  window.sideComments = new SideComments('#commentable-container' + scenarioIdStr, currentUser, comments);
}
