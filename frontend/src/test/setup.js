import '@testing-library/jest-dom'
import { vi } from 'vitest'

global.chrome = {
  tabs: {
    query: vi.fn((query, callback) => {
      callback([{ url: 'https://example.com' }])
    }),
  },
}
