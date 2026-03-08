import crypto from 'crypto';
import { TextEncoder, TextDecoder } from 'util';

global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

if (!global.crypto) global.crypto = {};
global.crypto.subtle = {
  digest: async (algorithm, data) => {
    const hash = crypto.createHash(algorithm.toLowerCase().replace('-', ''));
    hash.update(Buffer.from(data));
    return new Uint8Array(hash.digest());
  }
};
