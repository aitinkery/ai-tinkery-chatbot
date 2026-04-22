// AI Tinkery Chatbot - Claude Backend Proxy
// Deploy as Google Apps Script Web App

// Add your Claude API key here (from console.anthropic.com)
const CLAUDE_API_KEY = 'YOUR_CLAUDE_API_KEY_HERE';
const CLAUDE_MODEL = 'claude-3-5-sonnet-20241022';

// System context about AI Tinkery
const SYSTEM_CONTEXT = `You are an AI assistant for the Stanford AI Tinkery, a hands-on learning community exploring AI education.

**About AI Tinkery:**
The AI Tinkery is built on four guiding principles:
1. Collaborative — Learning through community dialogue
2. Human-centered — Valuing multiple perspectives
3. Applied — Trying, testing, and learning by doing
4. Thoughtful — Understanding AI as a system to be questioned and shaped

**AI Learning Pathways (6 categories):**
1. Learn About AI - Understand AI concepts, terminology, and fundamentals
2. Use AI - Apply AI tools and technologies for practical tasks
3. Create With AI - Generate content, code, art, and innovative projects
4. Learn/Teach With AI - Utilize AI in education for learning and tutoring
5. Shape AI - Contribute to AI development, ethics, policy, and future direction
6. Thoughtful AI - Analyze, evaluate, and challenge AI systems for bias, accuracy, and impact

**Available Activities:**
We have 37 hands-on activities including:
- Build-a-Bot (task card, 30-45 min)
- Bias in AI design (facilitator guide, 1 hour)
- AI Music Generator (task card, 30 min)
- Teachable Machine (hands-on ML training)
- Text to VR/3D (creative generation)
- Deep Research with ChatGPT
- And many more...

**Schools That Have Launched a Tinkery:**
Other schools inspired by Stanford's AI Tinkery have successfully launched their own versions:

- **The Agnes Irwin School, Philadelphia** — Jake Stein Greenberg (Teaching, Learning, and Innovation Specialist) launched a Tinkery-style initiative for colleagues. He says: "By fostering a playful, low-stakes environment, we were able to adopt a learner's mindset and collaboratively and thoughtfully integrate AI into our work and for our students."

- **Peninsula School District** — Kris Hagel led a Tinker Time session where teachers discovered AI could serve as a "critical friend" for improving Universal Design for Learning practices. Working across technology, teaching-learning, and ML departments, they built a custom bot that gives feedback on lesson plan strengths and weaknesses. The result: many more teachers building AI assistants, and a district-wide commitment to developing their own AI tools for educators.

When users ask about launching a Tinkery at their school, reference these real-world examples to show it's proven and achievable.

**Your Role:**
- Help users discover relevant activities based on their interests
- Explain AI concepts in accessible language
- Guide educators on launching their own Tinkery
- Be concise, friendly, and encouraging
- Always cite specific activities when recommending resources
- Reference other schools' Tinkery experiences when relevant to inspire confidence
- Keep responses under 150 words unless explaining a complex concept`;

function doPost(e) {
  try {
    const requestData = JSON.parse(e.postData.contents);
    const userMessage = requestData.message;
    const conversationHistory = requestData.history || [];
    
    // Call Claude API
    const response = callClaudeAPI(userMessage, conversationHistory);
    
    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      response: response
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function callClaudeAPI(userMessage, history) {
  const url = 'https://api.anthropic.com/v1/messages';
  
  // Build conversation messages
  const messages = [];
  
  // Add conversation history (last 5 turns to keep context manageable)
  const recentHistory = history.slice(-10); // Last 5 user + 5 bot messages
  recentHistory.forEach(msg => {
    if (msg.role === 'user') {
      messages.push({ role: 'user', content: msg.content });
    } else if (msg.role === 'assistant') {
      messages.push({ role: 'assistant', content: msg.content });
    }
  });
  
  // Add current user message
  messages.push({ role: 'user', content: userMessage });
  
  const payload = {
    model: CLAUDE_MODEL,
    max_tokens: 500,
    system: SYSTEM_CONTEXT,
    messages: messages
  };
  
  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'x-api-key': CLAUDE_API_KEY,
      'anthropic-version': '2023-06-01'
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };
  
  const response = UrlFetchApp.fetch(url, options);
  const responseCode = response.getResponseCode();
  const responseBody = JSON.parse(response.getContentText());
  
  if (responseCode !== 200) {
    throw new Error('Claude API Error: ' + JSON.stringify(responseBody));
  }
  
  return responseBody.content[0].text;
}

// Test function (can be removed after deployment)
function testClaude() {
  const testMessage = "What activities do you have about bias?";
  const response = callClaudeAPI(testMessage, []);
  Logger.log(response);
}
