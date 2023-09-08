function deleteMovie(movie_id, liked) {
    $.ajax({
        url: "/liked",
        type: "POST",
        dataType: "json",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({
            id: movie_id,
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

function update() {
    let rList = $(".rating-list");

    if (rList.children().length === 0) {
        rList.text("You don't have liked movies")
    }
}

$(document).ready(function() {
    let deleteMovieBtn = $(".delete-button");
    console.log(deleteMovieBtn);
    deleteMovieBtn.each(function(i, btn) {
        $(btn).click(function() {
            let movie_id = $(this).attr("data-id");
            console.log(movie_id);
            deleteMovie(movie_id, false);
            $(this).parent().remove();
            update();
        });
    })
    update();
});