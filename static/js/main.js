window.addToQMetry = async function(event) {
    const button = event.target;
    const testCasesData = JSON.parse(button.dataset.testCases);
    const ticketId = button.dataset.ticketId;

    // Limit the data size by only sending necessary fields
    const testCases = testCasesData.map(row => ({
        'Test Case ID': row['Test Case ID'],
        'Summary': row['Summary'].substring(0, 255),  // Limit summary length
        'Type': row['Type'],
        'Priority': row['Priority'],
        'Steps': row['Steps'].substring(0, 1000),  // Limit steps length
        'Expected Result': row['Expected Result'].substring(0, 1000)  // Limit expected result length
    }));

    // Disable the button to prevent double submission
    button.disabled = true;
    button.textContent = 'Adding to QMetry...';

    const maxRetries = 3;
    let retryCount = 0;

    while (retryCount < maxRetries) {
        try {
            const response = await fetch('/add-to-qmetry', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                credentials: 'same-origin',
                body: JSON.stringify({
                    test_cases: testCases,
                    ticket_id: ticketId
                })
            });

            // Handle non-JSON responses
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error('Server returned non-JSON response');
            }

            // Handle large responses
            const text = await response.text();
            let data;
            try {
                data = JSON.parse(text);
            } catch (e) {
                throw new Error('Invalid JSON response from server');
            }

            if (!response.ok) {
                throw new Error(data.message || `HTTP error! status: ${response.status}`);
            }

            if (data.success) {
                alert('Test cases added to QMetry successfully!');
                break;
            } else {
                throw new Error(data.message || 'Failed to add test cases to QMetry');
            }
        } catch (error) {
            console.error(`Attempt ${retryCount + 1} failed:`, error);
            retryCount++;

            if (retryCount === maxRetries) {
                alert('Error adding test cases to QMetry: ' + error.message + '\nPlease try again later.');
                break;
            }

            // Wait before retrying (exponential backoff)
            await new Promise(resolve => setTimeout(resolve, Math.pow(2, retryCount) * 1000));
            button.textContent = `Retrying... (${retryCount}/${maxRetries})`;
        }
    }

    // Re-enable the button
    button.disabled = false;
    button.textContent = 'Add to QMetry';
};

document.addEventListener("DOMContentLoaded", function () {
    // Add click event listeners to all "Add to QMetry" buttons
    document.querySelectorAll("button.add-to-qmetry").forEach(btn => {
        btn.addEventListener("click", addToQMetry);
    });
});

// Function to copy automation script to clipboard
window.copyToClipboard = function() {
    const codeElement = document.querySelector('pre code');
    if (codeElement) {
        const textToCopy = codeElement.textContent;
        
        // Use modern clipboard API if available
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(textToCopy).then(function() {
                showCopySuccess();
            }).catch(function(err) {
                console.error('Could not copy text: ', err);
                fallbackCopyTextToClipboard(textToCopy);
            });
        } else {
            fallbackCopyTextToClipboard(textToCopy);
        }
    }
};

function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    textArea.style.opacity = "0";
    
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showCopySuccess();
        } else {
            showCopyError();
        }
    } catch (err) {
        console.error('Fallback: Oops, unable to copy', err);
        showCopyError();
    }
    
    document.body.removeChild(textArea);
}

function showCopySuccess() {
    const button = document.querySelector('button[onclick="copyToClipboard()"]');
    const originalText = button.textContent;
    button.textContent = 'Copied!';
    button.classList.remove('bg-gray-500', 'hover:bg-gray-600');
    button.classList.add('bg-green-500', 'hover:bg-green-600');
    
    setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove('bg-green-500', 'hover:bg-green-600');
        button.classList.add('bg-gray-500', 'hover:bg-gray-600');
    }, 2000);
}

function showCopyError() {
    const button = document.querySelector('button[onclick="copyToClipboard()"]');
    const originalText = button.textContent;
    button.textContent = 'Failed!';
    button.classList.remove('bg-gray-500', 'hover:bg-gray-600');
    button.classList.add('bg-red-500', 'hover:bg-red-600');
    
    setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove('bg-red-500', 'hover:bg-red-600');
        button.classList.add('bg-gray-500', 'hover:bg-gray-600');
    }, 2000);
}

// Function to test webhook connectivity
window.testWebhooks = async function() {
    const resultsDiv = document.getElementById('webhook-results');
    const button = document.querySelector('button[onclick="testWebhooks()"]');
    
    // Disable button and show loading
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testing...';
    resultsDiv.innerHTML = '<div class="alert alert-info">Testing webhook connectivity...</div>';
    
    try {
        const response = await fetch('/test-webhooks', {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const results = await response.json();
        
        // Display results
        let html = '<div class="row">';
        
        // Teams result
        html += '<div class="col-md-6">';
        html += '<div class="card">';
        html += '<div class="card-header"><h6 class="mb-0"><i class="fab fa-microsoft"></i> Teams</h6></div>';
        html += '<div class="card-body">';
        if (results.teams.includes('✅')) {
            html += '<div class="alert alert-success">' + results.teams + '</div>';
        } else {
            html += '<div class="alert alert-danger">' + results.teams + '</div>';
        }
        html += '</div></div></div>';
        
        // Slack result
        html += '<div class="col-md-6">';
        html += '<div class="card">';
        html += '<div class="card-header"><h6 class="mb-0"><i class="fab fa-slack"></i> Slack</h6></div>';
        html += '<div class="card-body">';
        if (results.slack.includes('✅')) {
            html += '<div class="alert alert-success">' + results.slack + '</div>';
        } else {
            html += '<div class="alert alert-danger">' + results.slack + '</div>';
        }
        html += '</div></div></div>';
        
        html += '</div>';
        
        // Add setup instructions if webhooks are not configured
        if (results.teams.includes('not configured') || results.slack.includes('not configured')) {
            html += '<div class="mt-3">';
            html += '<div class="alert alert-warning">';
            html += '<h6><i class="fas fa-info-circle"></i> Setup Required</h6>';
            html += '<p>Follow the <a href="WEBHOOK_SETUP.md" target="_blank">Webhook Setup Guide</a> to configure your webhooks.</p>';
            html += '</div>';
            html += '</div>';
        }
        
        resultsDiv.innerHTML = html;
        
    } catch (error) {
        console.error('Error testing webhooks:', error);
        resultsDiv.innerHTML = '<div class="alert alert-danger">Error testing webhooks: ' + error.message + '</div>';
    } finally {
        // Re-enable button
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-vial"></i> Test Webhooks';
    }
}; 