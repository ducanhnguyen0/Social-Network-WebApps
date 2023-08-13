function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function save_changes(id) {
    const content = document.getElementById(`textarea_${id}`).value;
    const og_content = document.getElementById(`content_${id}`);
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {"Content-type":"application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            content: content
        })
    })
    .then(response => response.json())
    .then(result => {
        og_content.innerHTML = result;
    })
}


function like_post(id) {
    const icon = document.getElementById(`${id}`);
    if (icon.classList.contains('fa-heart')) {
        fetch(`/unlike/${id}`)
        .then(response => response.json())
        .then(result => {
            icon.classList.remove('fa-heart')
            icon.classList.add('fa-heart-o')
            if (result > 0) {
                document.querySelector(`#num_of_like_${id}`).innerHTML = result + " like(s)"
            } else {
                document.querySelector(`#num_of_like_${id}`).innerHTML = "Be the first one to like this post"
            }

        })
    }
    else {
        fetch(`/like/${id}`)
        .then(response => response.json())
        .then(result => {
            icon.classList.remove('fa-heart-o')
            icon.classList.add('fa-heart')
            if (result > 0) {
                document.querySelector(`#num_of_like_${id}`).innerHTML = result + " like(s)"
            } else {
                document.querySelector(`#num_of_like_${id}`).innerHTML = "Be the first one to like this post"
            }
        })
    }

}

