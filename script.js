document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Impede o envio do formulário

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === 'Admin' && password === 'admin') {
        // Redireciona para a próxima página se as credenciais estiverem corretas
        window.location.href = 'dashboard.html';
    } else {
        // Exibe mensagem de erro se as credenciais estiverem incorretas
        document.getElementById('error-message').textContent = 'Usuário ou senha incorretos!';
    }
});
