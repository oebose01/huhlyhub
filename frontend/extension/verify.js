import { sha256 } from './crypto-helper.js';

export async function verifyCurrentTab() {
  return new Promise((resolve, reject) => {
    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
      try {
        const url = tabs[0]?.url;
        if (!url) throw new Error('No active tab found');

        const hash = await sha256(url);
        const response = await fetch('http://localhost:8000/api/verify-content', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content_hash: hash })
        });
        const data = await response.json();
        resolve(data);
      } catch (error) {
        reject(error);
      }
    });
  });
}
