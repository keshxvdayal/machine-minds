function submitComment() {
    var content = document.getElementById("comment-input").value;
    var post_id = document.getElementById("post-id").value;
    
    fetch("/api/forum/post-comment", {
        method: "POST",
        body: JSON.stringify({content:content , post_id:post_id}),
        headers: {"Content-Type": "application/json"}
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {window.location.reload();}
        else {alert('Error posting comment');}
    });
}