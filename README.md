# AI Image Studio

Create stunning AI-generated images with customizable art styles and dimensions.

## Features

- **Multiple Art Styles**: Choose from Photorealistic, Oil Painting, Watercolor, Digital Art, Anime, and Cyberpunk styles
- **Custom Dimensions**: Adjust width and height from 256px to 1024px
- **Magic Enhance**: Automatically boost your prompt with professional keywords
- **Surprise Me**: Get random prompts and art styles for inspiration
- **Download Images**: Save generated images directly to your device
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Tech Stack

- **Frontend**: React 18
- **Styling**: TailwindCSS
- **Build Tool**: Vite
- **Image Generation**: Pollinations AI API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Himanshu90909/AI-Summer-Internship.git
cd AI-Summer-Internship
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open your browser and navigate to `http://localhost:5173`

## Build for Production

```bash
npm run build
```

This will create an optimized production build in the `dist` directory.

## Preview Production Build

```bash
npm run preview
```

## Project Structure

```
AI-Summer-Internship/
├── src/
│   ├── components/
│   │   ├── ImageGenerator.jsx
│   │   └── ImageGenerator.css
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
├── index.html
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

## How to Use

1. **Enter a Prompt**: Describe the image you want to create in the text area
2. **Choose Art Style**: Select from various art styles using the dropdown
3. **Adjust Dimensions**: Use sliders to set the width and height
4. **Enable Magic Enhance**: Toggle to automatically enhance your prompt
5. **Generate**: Click the "Generate" button to create your image
6. **Download**: Once generated, click "Download Image" to save it

## Pro Tips

- Be descriptive in your prompt for better results
- Adjust dimensions for different aspect ratios
- Enable Magic Enhance for professional-quality results
- Use "Surprise Me!" for creative inspiration

## API Integration

This project uses the Pollinations AI API for image generation. The API endpoint is:
```
https://image.pollinations.ai/prompt/{prompt}?width={width}&height={height}
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Himanshu90909

## Acknowledgments

- Powered by Pollinations AI
- Built with React & TailwindCSS
- Vite for fast development and building
