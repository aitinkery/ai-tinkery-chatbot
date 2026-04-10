# AI Tinkery Chatbot - Claude Integration Setup

## Overview
The chatbot now uses Claude AI (Anthropic) for intelligent, contextual responses via a secure Google Apps Script backend proxy.

## Prerequisites
- Google account
- Claude API key from [console.anthropic.com](https://console.anthropic.com)
- ~$3-5/month estimated API costs (based on typical usage)

## Step 1: Get Claude API Key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Navigate to **API Keys**
4. Create a new key (copy it - you won't see it again!)
5. Recommended: Set usage limits to prevent unexpected costs

## Step 2: Deploy Google Apps Script Backend

1. Open [script.google.com](https://script.google.com)
2. Click **New Project**
3. Name it: "AI Tinkery Claude Backend"
4. Delete the default code
5. Copy the code from `claude-backend.gs` in this repo
6. **Replace** `YOUR_CLAUDE_API_KEY_HERE` with your actual API key
7. Click **Deploy** > **New deployment**
   - Type: **Web app**
   - Description: "AI Tinkery Claude Proxy"
   - Execute as: **Me**
   - Who has access: **Anyone**
8. Click **Deploy**
9. **Copy the deployment URL** (looks like: `https://script.google.com/macros/s/ABC123.../exec`)
10. Click **Authorize access** and grant permissions

## Step 3: Update Chatbot

1. Open `index.html`
2. Find line ~1282: `const CLAUDE_BACKEND_URL = 'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE';`
3. Replace with your deployment URL from Step 2
4. Save and deploy

## Step 4: Test

Open the chatbot and try these queries:

### Basic Understanding
- "What's the difference between machine learning and AI?"
- "Explain what tinkering means in this context"

### Activity Recommendations
- "I want to teach my students about bias in AI"
- "Do you have anything about creating images with AI?"
- "What activities are good for beginners?"

### Tinkery Launch Support
- "How would I start a Tinkery at my university?"
- "What roles do I need for a Tinkery?"

### Complex Queries
- "My students are interested in ethics but also want to build things"
- "Can you recommend a 30-minute activity about how AI learns?"

## How It Works

```
User Message
    ↓
Chatbot (checks keyword patterns first)
    ↓
If no match → askClaude()
    ↓
Google Apps Script Backend (secure proxy)
    ↓
Claude API (Anthropic)
    ↓
Response with context about AI Tinkery
```

## Features

✅ **Contextual Understanding**: Claude knows about AI Tinkery's mission, activities, and philosophy  
✅ **Activity Recommendations**: Can suggest specific activities based on interests  
✅ **Conversation History**: Maintains context across multiple messages  
✅ **Smart Fallback**: If Claude fails, falls back to keyword matching  
✅ **Secure API Key**: Your Claude key stays in Google Apps Script, never exposed in client code  

## Cost Management

### Estimated Usage
- Average conversation: 5-10 messages
- Cost per message: ~$0.003 (input) + ~$0.015 (output)
- **~$0.05-0.10 per conversation**

### Setting Limits (Recommended)
1. In Claude Console > **Usage & Billing**
2. Set monthly spending limit: **$10-20**
3. Enable email alerts at 50% and 90%

### Monitoring
- Check Google Apps Script execution logs
- Monitor Claude usage in console.anthropic.com

## Troubleshooting

### "I'm having trouble connecting right now"
**Possible causes:**
- Google Apps Script deployment URL is wrong
- Claude API key is invalid
- Monthly spending limit reached
- Network/CORS issues

**Fix:**
1. Check browser console for errors (F12)
2. Verify `CLAUDE_BACKEND_URL` in index.html
3. Test backend directly: Go to the Apps Script URL in browser (should show `{"success":false}`)
4. Check Claude console for API errors

### Claude not responding intelligently
**Check:**
- System context in `claude-backend.gs` is properly set
- Conversation history is being passed correctly
- Not hitting token limits (max_tokens in backend)

### High API costs
**Solutions:**
- Increase keyword matching coverage before Claude fallback
- Add caching for common questions
- Reduce max_tokens in backend (currently 500)

## Advanced Configuration

### Adjust Claude's Personality
Edit the `SYSTEM_CONTEXT` in `claude-backend.gs`:
```javascript
const SYSTEM_CONTEXT = `You are an AI assistant for Stanford AI Tinkery...
[Add specific personality traits, tone, response style here]`;
```

### Change Model
In `claude-backend.gs`:
```javascript
const CLAUDE_MODEL = 'claude-3-5-sonnet-20241022'; // Most capable
// OR
const CLAUDE_MODEL = 'claude-3-haiku-20240307'; // Faster, cheaper
```

### Increase Response Length
```javascript
max_tokens: 500  // Increase to 1000 for longer responses
```

## Security Notes

✅ **API Key Protection**: Key stored in Google Apps Script, not client code  
✅ **Rate Limiting**: Consider adding per-user rate limits in Apps Script  
✅ **CORS**: Apps Script automatically handles cross-origin requests  
⚠️ **Anyone Can Call**: The Apps Script URL is public - consider adding authentication if needed

## Support

- **Claude API Docs**: https://docs.anthropic.com
- **Google Apps Script**: https://developers.google.com/apps-script
- **AI Tinkery**: https://github.com/aitinkery/ai-tinkery-chatbot

---

**Ready to deploy?** Follow Steps 1-4 above, then test with real questions! 🚀
