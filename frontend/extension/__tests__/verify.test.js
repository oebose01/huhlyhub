import sinon from 'sinon';
import { createHash } from 'crypto';
import { verifyCurrentTab } from '../verify.js';

describe('verifyCurrentTab', () => {
  let chromeMock, fetchMock;

  beforeEach(() => {
    global.chrome = {
      tabs: {
        query: sinon.stub()
      }
    };
    global.fetch = sinon.stub();
  });

  afterEach(() => {
    sinon.restore();
    delete global.chrome;
    delete global.fetch;
  });

  it('should fetch verification result and return data on success', async () => {
    const fakeTab = { url: 'https://example.com' };
    chrome.tabs.query.callsArgWith(1, [fakeTab]);

    const expectedHash = createHash('sha256').update('https://example.com').digest('hex');
    const fakeResponse = {
      ok: true,
      json: async () => ({ success: true, owner: '0x123', timestamp: 1609459200 })
    };
    fetch.resolves(fakeResponse);

    const result = await verifyCurrentTab();

    expect(chrome.tabs.query.calledWith({ active: true, currentWindow: true })).toBe(true);
    expect(fetch.calledOnce).toBe(true);
    const fetchCall = fetch.getCall(0);
    expect(fetchCall.args[0]).toBe('http://localhost:8000/api/verify-content');
    expect(fetchCall.args[1]).toMatchObject({
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content_hash: expectedHash })
    });
    expect(result).toEqual({ success: true, owner: '0x123', timestamp: 1609459200 });
  });

  it('should throw error when no active tab found', async () => {
    chrome.tabs.query.callsArgWith(1, []); // no tabs

    await expect(verifyCurrentTab()).rejects.toThrow('No active tab found');
    expect(fetch.called).toBe(false);
  });

  it('should throw error when fetch fails', async () => {
    const fakeTab = { url: 'https://example.com' };
    chrome.tabs.query.callsArgWith(1, [fakeTab]);

    fetch.rejects(new Error('Network error'));

    await expect(verifyCurrentTab()).rejects.toThrow('Network error');
  });

  it('should handle API returning non-200 response', async () => {
    const fakeTab = { url: 'https://example.com' };
    chrome.tabs.query.callsArgWith(1, [fakeTab]);

    const fakeResponse = {
      ok: false,
      status: 500,
      statusText: 'Internal Server Error'
    };
    fetch.resolves(fakeResponse);

    // The code expects response.json() to be called, but if ok is false, json() will throw?
    // Actually in our code, we call response.json() regardless. So if response is not ok, json() still works.
    // We should test that path by mocking a non-ok response that still has json body.
    // But fetch API: if not ok, json() can still be called (it reads body). So we need to handle that.
    // We'll mock json to return an error-like body.
    fakeResponse.json = async () => ({ success: false, error: 'Server error' });

    const result = await verifyCurrentTab();
    expect(result).toEqual({ success: false, error: 'Server error' });
  });

  it('should handle API returning success but no owner (e.g., not registered)', async () => {
    const fakeTab = { url: 'https://example.com' };
    chrome.tabs.query.callsArgWith(1, [fakeTab]);

    const fakeResponse = {
      ok: true,
      json: async () => ({ success: false, message: 'Content not found' })
    };
    fetch.resolves(fakeResponse);

    const result = await verifyCurrentTab();
    expect(result).toEqual({ success: false, message: 'Content not found' });
  });
});
