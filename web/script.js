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

            // Destroy previous Konva stages
            if (window.Konva) {
                const stages = window.Konva.stages;
                if (stages && stages.length > 0) {
                    [...stages].forEach(stage => stage.destroy());
                }
            }

            clearCanvas();

            const stageContainer = document.createElement('div');
            stageContainer.id = 'konva-container';
            canvasContainer.appendChild(stageContainer);

            function runInjectedScript() {
                console.log('Executing injected JavaScript...');
                const container = document.getElementById('konva-container');
                try {
                    const script = document.createElement('script');
                    script.type = 'text/javascript';
                    script.textContent = `
                        (function() {
                            const container = document.getElementById('konva-container');
                            ${jsOutput.textContent}
                        })();
                    `;
                    document.body.appendChild(script);
                    injectedScript = script;
                    updateStatus('JavaScript injected and executed successfully!', 'success');
                } catch (err) {
                    console.error('Error executing JavaScript:', err);
                    updateStatus('Error executing JavaScript: ' + err.message, 'error');
                }
            }

            function ensureKonvaLoaded(callback) {
                if (window.Konva) {
                    callback();
                } else {
                    const konvaScript = document.createElement('script');
                    konvaScript.src = 'https://unpkg.com/konva@9/konva.min.js';
                    konvaScript.onload = callback;
                    konvaScript.onerror = () => updateStatus('Failed to load KonvaJS', 'error');
                    document.head.appendChild(konvaScript);
                }
            }

            console.log('Preparing to inject JavaScript...');
            ensureKonvaLoaded(runInjectedScript);

        } catch (error) {
            console.error('Error injecting JavaScript:', error);
            updateStatus('Error injecting JavaScript: ' + error.message, 'error');
        }
    });
    
    // Initialize
    updateStatus('Ready to process YAML', 'info');
    injectButton.disabled = true;
});
