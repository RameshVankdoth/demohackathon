
    document.addEventListener('DOMContentLoaded', function() {
        const codeEditor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
            lineNumbers: true,
            mode: 'python',
            theme: 'default',
            autoCloseBrackets: true,
            matchBrackets: true,
            styleActiveLine: true,
            extraKeys: {
                "Ctrl-Space": "autocomplete"
            }
        });

        const languageSelector = document.getElementById('language');
        const themeSelector = document.getElementById('theme');
        const outputElement = document.getElementById('output');
        const testScore = document.getElementById('test-score');

        languageSelector.addEventListener('change', function() {
            codeEditor.setOption('mode', languageSelector.value === 'python' ? 'python' : 'text/x-java');
        });

        themeSelector.addEventListener('change', function() {
            codeEditor.setOption('theme', themeSelector.value);
        });

        document.getElementById('run-button').addEventListener('click', function() {
            const userCode = codeEditor.getValue();
            const language = languageSelector.value;

            fetch('/execute_code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code: userCode, language: language })
            })
            .then(response => response.json())
            .then(data => {
                outputElement.innerHTML = data.output ? `<pre><h1>${data.output}</h1></pre>` : `<pre style="color: red;">${data.error || 'Error executing code. Please try again.'}</pre>`;
            })
            .catch(error => {
                console.error('Error:', error);
                outputElement.innerHTML = '<pre style="color: red;">Error executing code. Please try again.</pre>';
            });
        });

        document.getElementById('submit-button').addEventListener('click', function() {
            const userCode = codeEditor.getValue();
            const language = languageSelector.value;

            fetch('/check_code', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ code: userCode, language: language })
            })
            .then(response => response.json())
            .then(data => {
                if (data.results) {
                    testScore.innerHTML = data.results.map((result, index) => `<div>Test Case ${index + 1}: ${result}</div>`).join('');
                }
                if (data.score) {
                    testScore.innerHTML += `<div>Score: ${data.score}</div>`;
                }
                
                showThankYouPopup();

                // End session logic here (if any)
                endSession();
            })
            .catch(error => {
                console.error('Error:', error);
                outputElement.innerHTML = '<pre style="color: red;">Error checking code. Please try again.</pre>';
            });
        });

        function showThankYouPopup() {
            // Create and show the thank you popup
            const thankYouPopup = document.createElement('div');
            thankYouPopup.textContent = 'Thank you! Your response has been recorded.';
            thankYouPopup.style.position = 'fixed';
            thankYouPopup.style.top = '50%';
            thankYouPopup.style.left = '50%';
            thankYouPopup.style.transform = 'translate(-50%, -50%)';
            thankYouPopup.style.backgroundColor = '#0f0f0f';
            thankYouPopup.style.color = '#fff';
            thankYouPopup.style.padding = '20px';
            thankYouPopup.style.border = '1px solid #0a0a0a';
            thankYouPopup.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.1)';
            thankYouPopup.style.zIndex = '1000';
            document.body.appendChild(thankYouPopup);

            // Redirect to dashboard after 10 seconds
            setTimeout(function() {
                document.body.removeChild(thankYouPopup); // Remove the thank you popup
                window.location.href = '/dashboard'; // Redirect to the dashboard
            }, 10000); // 10 seconds
        }

        function endSession() {
            // Implement any additional logic to end the session if needed
            console.log('Session ended.');
        }
    });