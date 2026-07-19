import { useState } from 'react'
import './App.css'
import ImageGenerator from './components/ImageGenerator'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <ImageGenerator />
    </div>
  )
}

export default App
