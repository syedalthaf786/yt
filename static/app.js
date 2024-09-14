// app.js
document.getElementById('downloadForm').addEventListener('submit', function (e) {
    e.preventDefault();
  spinner =document.getElementById('spinner');
  spinner.innerHTML="loading...."
    const videoUrl = document.getElementById('videoUrl').value;
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.innerHTML = '';
  
    fetch('/download', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: videoUrl }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Show download link
          spinner.innerHTML="Enter";
          statusMessage.innerHTML = `<a href="${data.download_link}" class="btn btn-success" download>Download Video</a>`;
        } else {
          // Show error message
          statusMessage.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
        }
      })
      .catch(error => {
        statusMessage.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
      });
  });
  