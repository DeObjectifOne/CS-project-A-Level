// delete function
function deleteTask(taskId) {
    //sends a request to the delete-task route
    fetch("/delete-task", {
        method: "POST",
        //the data is converted into a JSON string
        body: JSON.stringify({ taskId: taskId }), 
//the designated string is then promptly deleted       
}).then((_res) => {
window.location.href = "/";
});
}

//light + dark mode function
function saveMode(mode) {
    fetch('/save-mode', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // This header specifies that the request body contains JSON
        },
        body: JSON.stringify({ mode: mode }),  // Convert the mode object to a JSON string
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data.message);  // Log success message
        applyMode(mode);  // Apply the mode after saving
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
