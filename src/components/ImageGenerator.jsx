import { useState } from 'react'
import './ImageGenerator.css'

const ART_STYLES = [
  'Photorealistic',
  'Oil Painting',
  'Watercolor',
  'Digital Art',
  'Anime',
  'Cyberpunk'
]

export default function ImageGenerator() {
  const [prompt, setPrompt] = useState('')
  const [artStyle, setArtStyle] = useState('Photorealistic')
  const [width, setWidth] = useState(512)
  const [height, setHeight] = useState(512)
  const [magicEnhance, setMagicEnhance] = useState(false)
  const [loading, setLoading] = useState(false)
  const [generatedImage, setGeneratedImage] = useState(null)
  const [error, setError] = useState(null)

  const enhancePrompt = (text) => {
    if (!magicEnhance) return text
    const enhancements = ', professional, high quality, detailed, masterpiece, 4k, trending'
    return text + enhancements
  }

  const generateImage = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const enhancedPrompt = enhancePrompt(`${prompt} in ${artStyle} style`)
      
      // Using Pollinations API
      const imageUrl = `https://image.pollinations.ai/prompt/${encodeURIComponent(enhancedPrompt)}?width=${width}&height=${height}`
      
      setGeneratedImage(imageUrl)
    } catch (err) {
      setError('Failed to generate image. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleSurpriseMe = () => {
    const surprisePrompts = [
      'A serene mountain landscape at sunset',
      'A futuristic city with flying cars',
      'An underwater kingdom with glowing creatures',
      'A magical forest with ancient trees',
      'A space station orbiting a distant planet',
      'A steampunk airship in the clouds',
      'A cozy coffee shop in autumn',
      'A dragon guarding treasure in a cave'
    ]
    
    const randomPrompt = surprisePrompts[Math.floor(Math.random() * surprisePrompts.length)]
    setPrompt(randomPrompt)
    setArtStyle(ART_STYLES[Math.floor(Math.random() * ART_STYLES.length)])
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="mb-4">
            <div className="text-5xl mb-2">🎨</div>
            <h1 className="text-4xl font-bold text-white mb-2">AI Image Studio</h1>
            <p className="text-gray-300 text-lg">Create stunning AI-generated images</p>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Controls */}
          <div className="bg-slate-800 rounded-lg p-8 shadow-xl">
            <div className="space-y-6">
              {/* Prompt Input */}
              <div>
                <label className="block text-white font-semibold mb-2">Your Vision</label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="Describe the image you want to create..."
                  className="w-full h-24 px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-blue-500 focus:outline-none resize-none"
                />
              </div>

              {/* Art Style */}
              <div>
                <label className="block text-white font-semibold mb-2">Art Style</label>
                <select
                  value={artStyle}
                  onChange={(e) => setArtStyle(e.target.value)}
                  className="w-full px-4 py-2 bg-slate-700 text-white rounded-lg border border-slate-600 focus:border-blue-500 focus:outline-none"
                >
                  {ART_STYLES.map(style => (
                    <option key={style} value={style}>{style}</option>
                  ))}
                </select>
              </div>

              {/* Dimensions */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-white font-semibold mb-2">Width</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="range"
                      min="256"
                      max="1024"
                      step="64"
                      value={width}
                      onChange={(e) => setWidth(Number(e.target.value))}
                      className="flex-1"
                    />
                    <span className="text-white font-mono">{width}px</span>
                  </div>
                </div>
                <div>
                  <label className="block text-white font-semibold mb-2">Height</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="range"
                      min="256"
                      max="1024"
                      step="64"
                      value={height}
                      onChange={(e) => setHeight(Number(e.target.value))}
                      className="flex-1"
                    />
                    <span className="text-white font-mono">{height}px</span>
                  </div>
                </div>
              </div>

              {/* Magic Enhance */}
              <div className="flex items-center gap-3 bg-slate-700 p-4 rounded-lg">
                <input
                  type="checkbox"
                  id="enhance"
                  checked={magicEnhance}
                  onChange={(e) => setMagicEnhance(e.target.checked)}
                  className="w-5 h-5 cursor-pointer"
                />
                <label htmlFor="enhance" className="text-white font-semibold cursor-pointer flex-1">
                  ✨ Magic Enhance
                </label>
                <span className="text-gray-300 text-sm">Boost your prompt</span>
              </div>

              {/* Buttons */}
              <div className="flex gap-3">
                <button
                  onClick={generateImage}
                  disabled={loading}
                  className="flex-1 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-bold py-3 px-6 rounded-lg transition duration-200"
                >
                  {loading ? 'Generating...' : 'Generate'}
                </button>
                <button
                  onClick={handleSurpriseMe}
                  disabled={loading}
                  className="flex-1 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 text-white font-bold py-3 px-6 rounded-lg transition duration-200"
                >
                  Surprise Me!
                </button>
              </div>

              {/* Error Message */}
              {error && (
                <div className="bg-red-900 text-red-100 p-3 rounded-lg">
                  {error}
                </div>
              )}

              {/* Pro Tips */}
              <div className="bg-slate-700 p-4 rounded-lg">
                <p className="text-white font-semibold mb-2">Pro Tips:</p>
                <ul className="text-gray-300 text-sm space-y-1">
                  <li>• Be descriptive in your prompt</li>
                  <li>• Adjust dimensions for different aspect ratios</li>
                  <li>• Enable Magic Enhance for better results</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Image Display */}
          <div className="bg-slate-800 rounded-lg p-8 shadow-xl flex flex-col items-center justify-center min-h-96">
            {generatedImage ? (
              <div className="w-full">
                <img
                  src={generatedImage}
                  alt="Generated"
                  className="w-full rounded-lg shadow-lg fade-in"
                  style={{ maxHeight: '500px', objectFit: 'contain' }}
                />
                <button
                  onClick={() => {
                    const link = document.createElement('a')
                    link.href = generatedImage
                    link.download = 'ai-image.png'
                    link.click()
                  }}
                  className="w-full mt-4 bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition duration-200"
                >
                  Download Image
                </button>
              </div>
            ) : loading ? (
              <div className="text-center">
                <div className="text-4xl mb-4 loading">✨</div>
                <p className="text-white">Generating your image...</p>
              </div>
            ) : (
              <div className="text-center">
                <div className="text-6xl mb-4">🖼️</div>
                <p className="text-gray-300">Your generated image will appear here</p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-400 text-sm">
          <p>Powered by Pollinations AI • Built with React & TailwindCSS</p>
        </div>
      </div>
    </div>
  )
}
