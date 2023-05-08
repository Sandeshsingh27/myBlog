function titleRequired(param){
    let formName= param.concat('BlogForm');
    var empty = document.forms[formName]["title"].value;
    empty= empty.trim();
    if (empty == ""|| empty == null){
    alert("Title field cannot be empty.");
    return false;
    }
    return true;
}

// Back-to-top start
function toTop() {
    window.scrollTo(0, 0);
  }
  
  $(window).scroll(() => {
    const scroll = $(window).scrollTop();
  
    if (scroll >= 150) {
      $(".bttBtn").addClass("active");
    } else {
      $(".bttBtn").removeClass("active");
    }
  });
  // Back-to-top ends