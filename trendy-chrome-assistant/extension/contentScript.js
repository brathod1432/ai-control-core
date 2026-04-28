(() => {
  const supportedHost = location.hostname.includes("tradingview.com") || location.hostname.includes("finance.yahoo.com");

  if (!supportedHost) {
    return;
  }

  chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
    if (message?.type !== "GET_PAGE_CONTEXT") {
      return false;
    }

    sendResponse({
      title: document.title,
      url: location.href,
      host: location.hostname
    });

    return true;
  });
})();

