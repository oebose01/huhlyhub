import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const manifestPath = path.join(__dirname, '../manifest.json');

describe('Extension Manifest', () => {
  it('should exist and be valid JSON', () => {
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    expect(manifest).toBeDefined();
  });

  it('should have required fields for Manifest V3', () => {
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    expect(manifest.manifest_version).toBe(3);
    expect(manifest.name).toBe('huhlyhub Verifier');
    expect(manifest.version).toMatch(/^\d+\.\d+\.\d+$/);
    expect(manifest.permissions).toEqual(expect.arrayContaining(['activeTab', 'storage']));
    expect(manifest.action).toBeDefined();
    expect(manifest.action.default_popup).toBe('popup.html');
  });
});
