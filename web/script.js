document.addEventListener('DOMContentLoaded', () => {
    // DOM elements
    const yamlInput = document.getElementById('yamlInput');
    const submitButton = document.getElementById('submitYaml');
    const jsOutput = document.getElementById('jsOutput');
    const injectButton = document.getElementById('injectJs');
    const canvasContainer = document.getElementById('canvasContainer');
    const statusMessage = document.getElementById('statusMessage');
    
    // API endpoint (assuming the main API is running on port 8000)
    const apiUrl = 'http://localhost:8000/canvas';
    
    // Store the current canvas ID
    let currentCanvasId = null;
    
    // Keep track of the injected script element
    let injectedScript = null;
    
    // Function to update status message
    function updateStatus(message, type = 'info') {
        statusMessage.textContent = message;
        statusMessage.className = type;
    }
    
    // Function to clear the canvas container
    function clearCanvas() {
        while (canvasContainer.firstChild) {
            canvasContainer.removeChild(canvasContainer.firstChild);
        }
    }
    
    // Submit YAML to the API
    submitButton.addEventListener('click', async () => {
        const yaml = yamlInput.value.trim();
        
        if (!yaml) {
            updateStatus('Please enter YAML configuration', 'error');
            return;
        }
        
        try {
            updateStatus('Sending YAML to API...', 'info');
            
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-yaml',
                },
                body: yaml
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to process YAML');
            }
            
            const data = await response.json();
            currentCanvasId = data.id;
            
            // Display the generated JavaScript
            jsOutput.textContent = data.jsCode || '// No JavaScript generated';
            
            updateStatus('JavaScript generated successfully!', 'success');
            injectButton.disabled = false;
        } catch (error) {
            console.error('Error:', error);
            jsOutput.textContent = '// Error: ' + error.message;
            updateStatus('Error: ' + error.message, 'error');
            injectButton.disabled = true;
        }
    });
    
    // Inject JavaScript into the page
    injectButton.addEventListener('click', () => {
        if (!jsOutput.textContent || jsOutput.textContent === '// JavaScript will appear here') {
            updateStatus('No JavaScript to inject', 'error');
            return;
        }
        
        try {
            // Clean up any previously injected script
            if (injectedScript && injectedScript.parentNode) {
                injectedScript.parentNode.removeChild(injectedScript);
                injectedScript = null;
            }
            
            // Clean up any Konva stages that might exist
            // This is important as Konva can leave event listeners and other resources
            if (window.Konva) {
                const stages = window.Konva.stages;
                if (stages && stages.length > 0) {
                    // Make a copy of the array since destroy() modifies the original array
                    [...stages].forEach(stage => stage.destroy());
                }
            }
            
            // Clear previous canvas
            clearCanvas();
            
            // Create a container for the Konva stage
            const stageContainer = document.createElement('div');
            stageContainer.id = 'konva-container';
            canvasContainer.appendChild(stageContainer);
            
            // For debugging
            console.log('Injecting JavaScript:', jsOutput.textContent);
            
            // Use eval in a controlled way to execute the code
            // First create a function that will execute in the global scope
            const executeCode = new Function(`
                try {
                    // Create a safe execution context
                    (function() {
                        // Make sure the container is available to the code
                        const container = document.getElementById('konva-container');
                        
                        // Execute the code
                        ${jsOutput.textContent}
                    })();
                    return true;
                } catch (error) {
                    console.error('Error executing injected JavaScript:', error);
                    document.getElementById('statusMessage').textContent = 'Error executing JavaScript: ' + error.message;
                    document.getElementById('statusMessage').className = 'error';
                    return false;
                }
            `);
            
            // Execute the code
            const success = executeCode();
            
            if (success) {
                updateStatus('JavaScript injected and executed successfully!', 'success');
            }
        } catch (error) {
            console.error('Error injecting JavaScript:', error);
            updateStatus('Error injecting JavaScript: ' + error.message, 'error');
        }
    });
    
    // Initialize
    updateStatus('Ready to process YAML', 'info');
    injectButton.disabled = true;
});
