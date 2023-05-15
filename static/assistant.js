document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#chat-form');
    const prompt = document.querySelector('#prompt')
    const messageList= document.querySelector('#messages-list');
    spinner.style.display = 'none';

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      spinner.style.display = 'inline-block';
      send.style.display = 'none';
      const message = prompt.value;
      prompt.value = '';
      const query = document.createElement('div');
      query.className = 'query';
      query.textContent = 'You: ' + message;
      messageList.appendChild(query);

      fetch(`http://127.0.0.1:5000/api?query=${encodeURIComponent(message)}`)
        .then((response) => response.text())
        .then((text) => {
          spinner.style.display = 'none';
          send.style.display = 'inline';
          const response = document.createElement('div');
          response.className = 'response';
          response.innerHTML = 'AI: ' + marked.parse(text);
          messageList.appendChild(response);});
    });
});
