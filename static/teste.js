document.getElementById('loginForm').addEventListener('submit', (event) => {
  event.preventDefault();

  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const errorMessage = document.getElementById('error-message');

  const username = usernameInput.value.trim();
  const password = passwordInput.value;

  // Validação básica
  if (!username || !password) {
    errorMessage.textContent = 'Por favor, preencha todos os campos.';
    return;
  }

  // Verificação de credenciais (substitua por sua lógica de autenticação)
  if (username === 'Admin' && password === 'admin') {
    // Redirecionamento
    window.location.href = '/dashboard';
  } else {
    // Exibe mensagem de erro se as credenciais estiverem incorretas
    document.getElementById('error-message').textContent = 'Usuário ou senha incorretos!';
  }
});
