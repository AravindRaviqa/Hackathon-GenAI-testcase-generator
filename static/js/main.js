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