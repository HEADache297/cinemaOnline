function sendData(movie_id, movie_name, liked) {
    $.ajax({
        url: "/liked",
        type: "POST",
        dataType: "json",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({
            id: movie_id,
            name: movie_name,
            liked: liked
        }),
        // success: function() {
        //     alert("success!");
        // },
        error: function(r, status, error) {
            alert(error);
            console.log(error);
        }
      });
}

$(document).ready(function() {
    let liked = $(".liked");
    let unliked = $(".unliked");

    let movie_id = liked.parent().attr("data-id");
    let movie_name = liked.parent().attr("data-name");

    liked.click(function() {
        $(this).hide();
        unliked.show();
        sendData(movie_id, movie_name, false);
    });

    unliked.click(function() {
        $(this).hide();
        liked.show();
        sendData(movie_id, movie_name, true);
    });
});