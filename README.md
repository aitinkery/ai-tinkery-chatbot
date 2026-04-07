# AI Tinkery Chatbot

An interactive chatbot to help people learn about the AI Tinkery at Stanford and discover hands-on AI learning activities.

## Features

- **Conversational Interface** — Natural, friendly chat experience
- **Smart Onboarding** — Captures user name and affiliation for tracking
- **Activity Recommendations** — Suggests activities based on user interests using keyword matching
- **26 Activities** — Full catalog of AI Tinkery activities with links
- **Persistent State** — Remembers user info and conversation across sessions
- **Guided Experience** — Helps users who aren't sure how to navigate
- **AI Tinkery Branding** — Orange/black color scheme, Bungee font

## What It Does

1. **Welcome & Onboard** — Greets users and collects their name and affiliation
2. **Educate** — Teaches about the AI Tinkery's mission, principles, and approach
3. **Recommend** — Suggests relevant activities based on user interests
4. **Guide** — Walks users through activity details and provides links to full guides
5. **Connect** — Shares info about the Satellite Network and community

## Activity Categories

Activities are organized into six pedagogical categories:
- **Learn About AI** — Understanding what AI is and how it works
- **Use AI** — Practical application of AI tools
- **Create With AI** — Building things using AI
- **Learn/Teach With AI** — AI as an educational tool
- **Shape AI** — Thinking about AI's future and design
- **Critique AI** — Examining AI's impact, bias, ethics, and limitations

## User Experience

The chatbot is designed to be:
- **Approachable** — Friendly tone, no jargon
- **Helpful** — Quick replies guide uncertain users
- **Smart** — Keyword matching recommends relevant activities
- **Informative** — Rich content about the Tinkery and its approach
- **Actionable** — Direct links to activity guides

## Tech Stack

- **Single HTML file** — No dependencies beyond CDN fonts
- **Vanilla JavaScript** — No frameworks
- **LocalStorage** — Persistent user state
- **Responsive Design** — Mobile-friendly interface
- **AI Tinkery Branding** — Orange (#E8620A), black, Bungee + Source Sans 3 fonts

## Deployment

Deploy to:
- **Netlify** — Drag and drop the HTML file
- **Vercel** — Deploy via CLI or GitHub integration
- **GitHub Pages** — Push to a repo and enable Pages
- **Replit** — Import as HTML/CSS/JS project

## Usage Tracking

The chatbot captures:
- User name
- Affiliation (school/organization)
- Activities explored
- Interests expressed
- Full conversation history

All data is stored in the browser's `localStorage` under the key `aiTinkeryState`.

To export user data for analysis, users can run this in the browser console:
```javascript
console.log(JSON.parse(localStorage.getItem('aiTinkeryState')));
```

## Customization

To update activities, edit the `ACTIVITIES` array in the JavaScript section. Each activity has:
- `name` — Activity title
- `type` — Format (Task Card, Slide Deck, etc.)
- `time` — Duration estimate
- `audience` — Target users (Teacher, Student)
- `description` — Brief summary
- `link` — Google Doc/Slides link
- `category` — Pedagogical category
- `keywords` — For recommendation matching

## Replacing Previous Sites

This chatbot replaces:
- https://delightful-swan-cce030.netlify.app/
- https://stanford-ai-tinkery-checkinboard-lab114.replit.app/

It provides a more conversational, guided experience compared to static forms or grids.

## About the AI Tinkery

The AI Tinkery at Stanford is a space to play and tinker with AI — to better understand, use, and shape it. Part of the Stanford Accelerator for Learning at the Graduate School of Education.

**Learn more:** [ai-tinkery.stanford.edu](https://ai-tinkery.stanford.edu)

**Authors:**
- Gregory Wilson (Manager)
- Dr. Karin Forssell (Director)

---

Built with 🔧 for the AI Tinkery at Stanford
