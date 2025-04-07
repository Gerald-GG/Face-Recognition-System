const video = document.getElementById('webcam');
const canvas = document.getElementById('snapshot');
const resultBox = document.getElementById('resultBox');

// Start the webcam
function startWebcam() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      video.srcObject = stream;
    })
    .catch(err => {
      alert("Webcam access error: " + err.message);
    });
}

// Capture image from webcam
function captureImage() {
  const ctx = canvas.getContext('2d');
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0);

  const base64Image = canvas.toDataURL('image/png');
  sendImageToBackend(base64Image);
}

// Upload an image file
function uploadImage(event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function () {
    sendImageToBackend(reader.result);
  };
  reader.readAsDataURL(file);
}

// Send base64 image to Flask backend
function sendImageToBackend(base64Image) {
  resultBox.innerText = "⏳ Detecting face...";

  fetch('http://localhost:5000/detect', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ image: base64Image })
  })
  .then(response => response.json())
  .then(data => {
    if (data.result) {
      resultBox.innerText = "✅ Result: " + data.result;
    } else {
      resultBox.innerText = "❌ No face detected or match not found.";
    }
  })
  .catch(error => {
    resultBox.innerText = "🚨 Error: " + error.message;
  });
}
