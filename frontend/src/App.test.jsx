import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders the huhlyhub heading', () => {
    render(<App />)
    expect(screen.getByText(/huhlyhub/i, { selector: 'h1' })).toBeInTheDocument()
  })
})
