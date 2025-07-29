# Houzz Website Clone

A React.js frontend clone of Houzz.in with similar functionality and design.

## Features

- **Header Navigation**: Search functionality, navigation menu, and authentication buttons
- **Hero Section**: Three main action cards (Discover Ideas, Browse Pros, Suggest Pros)
- **Browse by Room**: Interactive room categories with hover effects
- **Latest Stories**: Article cards with categories and read times
- **Responsive Design**: Mobile-friendly layout that adapts to different screen sizes

## Project Structure

```
src/
├── components/
│   ├── Header.js          # Navigation header
│   ├── Header.css         # Header styles
│   ├── HeroSection.js     # Main action cards section
│   ├── HeroSection.css    # Hero section styles
│   ├── BrowseByRoom.js    # Room categories section
│   ├── BrowseByRoom.css   # Room browsing styles
│   ├── LatestStories.js   # Article cards section
│   └── LatestStories.css  # Stories section styles
├── App.js                 # Main application component
├── App.css               # Global styles and utilities
├── index.js              # Application entry point
└── index.css             # Base styles
```

## Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Next Steps

1. **Add Images**: Replace placeholder image paths with actual images
2. **Backend Integration**: Integrate with Crawl4AI Python backend for content scraping
3. **Routing**: Add React Router for navigation between pages
4. **State Management**: Implement context or Redux for global state
5. **API Integration**: Connect to backend APIs for dynamic content
6. **Search Functionality**: Implement actual search with backend
7. **Authentication**: Add real authentication system
8. **Professional Profiles**: Add professional listing pages
9. **Photo Galleries**: Implement photo browsing functionality
10. **Content Management**: Add CMS for dynamic content updates

## Technologies Used

- React.js 18
- CSS3 with Grid and Flexbox
- Responsive Design
- Modern ES6+ JavaScript

## Future Backend Integration

The frontend is designed to easily integrate with a Python backend using Crawl4AI for:
- Content scraping from Houzz.in
- Dynamic content updates
- Search functionality
- Professional listings
- Photo galleries
- User-generated content