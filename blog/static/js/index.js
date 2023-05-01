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