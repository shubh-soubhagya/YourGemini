document.getElementById('ai-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const prompt = document.getElementById('prompt').value;
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                'prompt': prompt
            })
        });
        const data = await response.json();
        document.getElementById('ai-response').innerHTML = marked.parse(data.content);
    } catch (error) {
        document.getElementById('ai-response').innerHTML = `<pre>Error: ${error.message}</pre>`;
    }
});
