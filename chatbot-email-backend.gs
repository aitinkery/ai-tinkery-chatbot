/**
 * Google Apps Script to send email notifications
 * when users sign up via the AI Tinkery chatbot
 * 
 * DEPLOYMENT INSTRUCTIONS:
 * 1. Go to script.google.com
 * 2. Create new project
 * 3. Paste this code
 * 4. Deploy > New deployment
 * 5. Type: Web app
 * 6. Execute as: Me
 * 7. Who has access: Anyone
 * 8. Deploy and copy the URL
 * 9. Replace 'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE' in index.html
 */

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const name = data.name || 'Unknown';
    const affiliation = data.affiliation || 'Not provided';
    const timestamp = data.timestamp || new Date().toLocaleString();
    
    // Email details
    const recipient = 'lab1@aitinkery.com';
    const subject = 'New AI Tinkery Chatbot User';
    const body = `
New user signed up on the AI Tinkery Chatbot:

Name: ${name}
Affiliation: ${affiliation}
Timestamp: ${timestamp}

---
This email was automatically sent from the AI Tinkery Chatbot.
    `.trim();
    
    // Send email
    MailApp.sendEmail(recipient, subject, body);
    
    return ContentService
      .createTextOutput(JSON.stringify({ success: true }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ 
        success: false, 
        error: error.toString() 
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Test function
function test() {
  const testData = {
    postData: {
      contents: JSON.stringify({
        name: 'Test User',
        affiliation: 'Test School',
        timestamp: new Date().toLocaleString()
      })
    }
  };
  
  doPost(testData);
}
