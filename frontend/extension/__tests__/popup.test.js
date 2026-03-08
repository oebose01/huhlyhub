import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

describe('Popup', () => {
  let popupHtml;
  let popupJs;

  beforeAll(() => {
    popupHtml = fs.readFileSync(path.join(__dirname, '../popup.html'), 'utf8');
    popupJs = fs.readFileSync(path.join(__dirname, '../popup.js'), 'utf8');
  });

  beforeEach(() => {
    document.body.innerHTML = popupHtml;
    // Execute the script in the test environment
    const script = document.createElement('script');
    script.textContent = popupJs;
    document.body.appendChild(script);
  });

  it('should have a verify button', () => {
    const button = document.getElementById('verify');
    expect(button).not.toBeNull();
  });

  it('should display "Verifying..." when button is clicked', () => {
    const button = document.getElementById('verify');
    const resultDiv = document.getElementById('result');
    button.click();
    expect(resultDiv.textContent).toBe('Verifying...');
  });
});
