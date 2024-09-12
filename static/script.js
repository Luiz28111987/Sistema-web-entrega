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
  
    // Código para a página de inserir entrega (inserir_entrega.html)
    if ($("#numero_entrega").length > 0) {
        // Quando a página carregar, buscar o próximo número de entrega
        $.get("/numero_entrega", function(data) {
            $("#numero_entrega").val(data.proximo_id);  // Preenche o campo com o proximo_id retornado
        });
  
        // Debounce para sugestão de placas
        let debounceTimeoutPlaca;
        $("#busca-placa").on("input", function() {
            clearTimeout(debounceTimeoutPlaca);
            var termo = $(this).val();
            debounceTimeoutPlaca = setTimeout(function() {
                $.get("/sugestoes-placa", { termo: termo })
                .done(function(data) {
                    $("#sugestoes-placa").empty();
                    $.each(data, function(index, value) {
                        $("#sugestoes-placa").append("<li class='sugestao-placa'>" + value + "</li>");
                    });
                });
            }, 300);
        });
  
        // Seleção de placa
        $(document).on("click", ".sugestao-placa", function() {
            var placaSelecionada = $(this).text();
            $("#busca-placa").val(placaSelecionada);
            $("#sugestoes-placa").empty();
  
            // Fazer a requisição para buscar o tipo de veículo com base na placa
            $.get("/get-tipo-veiculo", { placa: placaSelecionada })
            .done(function(data) {
                if (data.tipo_veiculo) {
                    $("#veiculo").val(data.tipo_veiculo);
                }
            })
            .fail(function() {
                alert("Tipo de veículo não encontrado");
            });
        });
  
        // Debounce para sugestão de motoristas
        let debounceTimeoutMotorista;
        $("#busca-motorista").on("input", function() {
            clearTimeout(debounceTimeoutMotorista);
            var termo = $(this).val();
            debounceTimeoutMotorista = setTimeout(function() {
                $.get("/sugestoes-motorista", { termo: termo })
                .done(function(data) {
                    $("#sugestoes-motorista").empty();
                    $.each(data, function(index, value) {
                        $("#sugestoes-motorista").append("<li class='sugestao-motorista'>" + value + "</li>");
                    });
                });
            }, 300);
        });
  
        // Seleção de motorista
        $(document).on("click", ".sugestao-motorista", function() {
            var motoristaSelecionado = $(this).text();
            $("#busca-motorista").val(motoristaSelecionado);
            $("#sugestoes-motorista").empty();
        });
  
        // Carregar todas as regiões quando a página é carregada
        $.get("/todas-regioes", function(data) {
            window.regioesDisponiveis = data;
        });
  
        // Debounce para sugestão de regiões
        let debounceTimeoutRegiao;
        $("#busca-regiao").on("input", function() {
            clearTimeout(debounceTimeoutRegiao);
            var termo = $(this).val();
            debounceTimeoutRegiao = setTimeout(function() {
                let regioesFiltradas = window.regioesDisponiveis.filter(function(regiao) {
                    return regiao.toLowerCase().includes(termo.toLowerCase());
                });
                $("#sugestoes-regiao").empty();
                $.each(regioesFiltradas, function(index, value) {
                    $("#sugestoes-regiao").append("<li class='sugestao-regiao'>" + value + "</li>");
                });
            }, 300);
        });
  
        // Seleção de região e adição automática à lista
        $(document).on("click", ".sugestao-regiao", function() {
            var regiaoSelecionada = $(this).text().trim();
            const buscaRegiao = $("#busca-regiao");
            const regioesAtuais = buscaRegiao.val();
            const regioesArray = regioesAtuais.split('/').map(regiao => regiao.trim()).filter(Boolean);
  
            if (!regioesArray.includes(regiaoSelecionada)) {
                regioesArray.push(regiaoSelecionada);
                buscaRegiao.val('');  // Limpa o campo de busca
  
                // Adicionar à lista de regiões selecionadas
                const li = document.createElement('li');
                li.textContent = regiaoSelecionada;
                $("#itemList").append(li);
            }
  
            $("#sugestoes-regiao").empty(); // Limpar sugestões
        });
  
        // Função para atualizar o campo de entrada com as regiões selecionadas
        function atualizarCampoRegioes() {
            const regioes = [];
            $("#itemList li").each(function() {
                regioes.push($(this).text());
            });
            $("#busca-regiao").val(regioes.join('/'));
        }
  
        // Adicionar listener para o envio do formulário
        $("form").on("submit", function() {
            atualizarCampoRegioes();
        });
  
        // Função para limpar todas as regiões selecionadas
        $("#limpar-regioes").click(function() {
            $("#itemList").empty();  // Limpar a lista de regiões
            $("#busca-regiao").val(''); // Limpar o campo de busca
        });
    }
  });