import { verifyCurrentTab } from './verify.js';

document.getElementById('verify').addEventListener('click', async () => {
  const resultDiv = document.getElementById('result');
  resultDiv.textContent = 'Verifying...';

  try {
    const data = await verifyCurrentTab();

    if (data.success && data.owner) {
      const date = new Date(data.timestamp * 1000).toLocaleString();
      resultDiv.innerHTML = `✅ Registered<br>Owner: ${data.owner}<br>Time: ${date}`;
    } else {
      resultDiv.textContent = '❌ Not registered on blockchain';
    }
  } catch (error) {
    resultDiv.textContent = `Error: ${error.message}`;
  }
});
