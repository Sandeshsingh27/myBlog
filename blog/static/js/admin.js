document.addEventListener("DOMContentLoaded", function (event) {
    let sc = document.createElement('script');
    sc.setAttribute('src', "https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js");

    document.head.appendChild(sc);


    sc.onload=()=>{
        tinymce.init({
            selector: '#id_content',
            // width: 600, // removing width will make the this field responsive and will take 100% of screen size
            height: 300,
            plugins: [
              'advlist', 'autolink', 'link', 'image', 'lists', 'charmap', 'preview', 'anchor', 'pagebreak',
              'searchreplace', 'wordcount', 'visualblocks', 'visualchars', 'code', 'fullscreen', 'insertdatetime',
              'media', 'table', 'emoticons', 'template', 'help'
            ],
            toolbar: 'undo redo | styles | bold italic | alignleft aligncenter alignright alignjustify | ' +
              'bullist numlist outdent indent | link image | print preview media fullscreen | ' +
              'forecolor backcolor emoticons | help',
            menu: {
              favs: { title: 'My Favorites', items: 'code visualaid | searchreplace | emoticons' }
            },
            menubar: 'favs file edit view insert format tools table help',
            content_css: 'css/content.css'
        });
    }
});  
