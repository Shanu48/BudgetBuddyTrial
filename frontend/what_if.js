document.getElementById('whatIfForm').addEventListener('submit', function(e) {
    e.preventDefault();

    const userId = document.getElementById('user_id').value;
    const question = document.getElementById('question').value;

    fetch('http://localhost:5000/api/what_if', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userId,
            question: question
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Add this line to log the response
        if (data.response) {
            document.getElementById('response').innerText = data.response;
        } else {
            document.getElementById('response').innerText = 'No response from backend.';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('response').innerText = 'An error occurred. Please try again.';
    });
});
