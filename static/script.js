$(document).ready(function() {
    // Código para a página de login (login.html)
    const loginForm = document.getElementById('loginForm');
  
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
  
            const usernameInput = document.getElementById('username');
            const passwordInput = document.getElementById('password');
            const errorMessage = document.getElementById('error-message');
  
            const username = usernameInput.value.trim();
            const password = passwordInput.value;
  
            if (!username || !password) {
                errorMessage.textContent = 'Por favor, preencha todos os campos.';
                return;
            }
  
            if (username === 'Admin' && password === 'admin') {
                window.location.href = '/dashboard';
            } else {
                errorMessage.textContent = 'Usuário ou senha incorretos!';
            }
        });
    }
  
    // Código para a página de finalizar entrega (finalizar_entrega.html)
    const botoesAlterar = document.querySelectorAll('.alterar');
    if (botoesAlterar.length > 0) {
        botoesAlterar.forEach(botao => {
            botao.addEventListener('click', () => {
                const idEntrega = botao.dataset.id;
                const url = `/editar_entrega/${idEntrega}`;
                window.location.href = url;
            });
        });  
    }
  });