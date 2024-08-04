function submitComment() {
    let comment_input = document.getElementById("comment-input");
    let content = comment_input.value;
    let post_id = document.getElementById("post-id").value;
    
    fetch("/api/forum/post-comment", {
        method: "POST",
        body: JSON.stringify({content:content , post_id:post_id}),
        headers: {"Content-Type": "application/json"}
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            comment_input.value = "";
            window.location.reload();
        }
        else {alert('Error posting comment');}
    });
}