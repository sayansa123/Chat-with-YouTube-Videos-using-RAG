const askButton = document.getElementById("askBtn");
const statusText = document.getElementById("status");
const answerBox = document.getElementById("answer");
const questionInput = document.getElementById("question");

let videoId = null;

initializePopup();

function initializePopup() {
  readVideoIdFromStorage();
}
function readVideoIdFromStorage() {
  chrome.storage.local.get(["video_id"], onVideoIdLoaded);
}
async function onVideoIdLoaded(result) {
  if (!result.video_id) {
    updateStatus("No YouTube video detected.");
    return;
  }
  videoId = result.video_id;
  updateStatus("Loading video…");
  await loadVideoInBackend();
}
async function loadVideoInBackend() {
  try {
    const response = await fetch(
      `http://localhost:8000/load_video?video_id=${videoId}`
    );

    if (response.ok) { 
      updateStatus("Video ready.");
    } else {
      updateStatus("Video already loaded.");
    }
    askButton.disabled = false;
    askButton.addEventListener("click", onAskClicked);
  } catch (error) {
    console.error(error);
    updateStatus("Backend not reachable.");
  }
}
async function onAskClicked() {
  const question = questionInput.value.trim();
  if (question === "") return;
  showAnswer("Thinking…");
  await sendQuestionToBackend(question);
}
async function sendQuestionToBackend(question) {
  try {
    const response = await fetch(
      `http://localhost:8000/ask?video_id=${videoId}&query=${encodeURIComponent(question)}`
    );
    const data = await response.json();
    showAnswer(data.message || "No answer received.");
  } catch (error) {
    console.error(error);
    showAnswer("Error getting answer.");
  }
}

function updateStatus(message) {
  statusText.innerText = message;
}
function showAnswer(message) {
  answerBox.innerText = message;
}