$(document).ready(function(){
  var SideComments = require('side-comments');
  window.sideComments = new SideComments('#commentable-container', currentUser, existingCommentsX);
/*  window.sideComments.on('commentPosted', function( comment ) {
    comment.id = parseInt(Math.random() * (100000 - 1) + 1);
    sideComments.insertComment(comment);
  });
  window.sideComments.on('commentDeleted', function( comment ) {
    sideComments.removeComment(comment.sectionId, comment.id);
  });
  */
});
