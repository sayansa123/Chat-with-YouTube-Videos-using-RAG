chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  if (changeInfo.url && changeInfo.url.includes("youtube.com/watch")) {
    const videoId = extractVideoId(changeInfo.url);
    if (!videoId) return;
    chrome.storage.local.set({ video_id: videoId });
    console.log("Background stored video_id:", videoId);
  }
});

function extractVideoId(url) {
  const urlObj = new URL(url);
  return urlObj.searchParams.get("v");
}
