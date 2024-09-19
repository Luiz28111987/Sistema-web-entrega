document.addEventListener('DOMContentLoaded', () => {
    // Verifica se o campo de número de entrega está presente na página
    if (document.getElementById("numero_entrega")) {
        // Quando a página carregar, buscar o próximo número de entrega
        $.get("/numero_entrega", function(data) {
            // Preenche o campo com o `proximo_id` retornado
            $("#numero_entrega").val(data.proximo_id);
        });
    }

    // Função para carregar sugestões de motoristas, placas e regiões
    async function carregarSugestoes(url, elementoId) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Erro na resposta da API: ${response.statusText}`);
            }
            const sugestoes = await response.json();
            const select = document.getElementById(elementoId);
            select.innerHTML = '<option value="">Selecione...</option>';

            sugestoes.forEach(sugestao => {
                const option = document.createElement('option');
                option.value = sugestao;
                option.textContent = sugestao;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('Erro ao carregar sugestões:', error);
        }
    }

    // Carregar sugestões
    carregarSugestoes('/sugestoes_motoristas', 'motorista');
    carregarSugestoes('/sugestoes_placas', 'placa');
    carregarSugestoes('/sugestoes_regioes', 'regiao');

    // Event listener para mudança na placa
    document.getElementById('placa').addEventListener('change', function() {
        const placaSelecionada = this.value;

        if (placaSelecionada) {
            // Fazer a requisição para buscar o tipo de veículo com base na placa
            $.get("/get-tipo-veiculo", { placa: placaSelecionada })
                .done(function(data) {
                    if (data.tipo_veiculo) {
                        $("#veiculo").val(data.tipo_veiculo);
                    } else {
                        $("#veiculo").val(''); // Limpar o campo se não encontrar tipo de veículo
                    }
                })
                .fail(function() {
                    alert("Tipo de veículo não encontrado");
                    $("#veiculo").val(''); // Limpar o campo em caso de falha
                });
        }
    });

    // Array para armazenar as regiões selecionadas
    let regioesSelecionadas = [];

    // Adicionar região à lista
    document.getElementById('adicionar_regiao').addEventListener('click', () => {
        const regiaoSelecionada = document.getElementById('regiao').value;
        if (regiaoSelecionada) {
            // Adicionar região ao array
            regioesSelecionadas.push(regiaoSelecionada);

            // Atualizar a lista visível no HTML
            const itemList = document.getElementById('itemList');
            const listItem = document.createElement('li');
            listItem.textContent = regiaoSelecionada;
            itemList.appendChild(listItem);

            // Atualizar o campo oculto com as regiões selecionadas
            document.getElementById('regioes_input').value = regioesSelecionadas.join('/');
            
            // Limpar a seleção após adicionar
            document.getElementById('regiao').value = '';
        } else {
            alert('Por favor, selecione uma região.');
        }
    });

    // Limpar regiões selecionadas
    document.getElementById('limpar-regioes').addEventListener('click', () => {
        // Limpar o array de regiões
        regioesSelecionadas = [];

        // Limpar a lista visível no HTML
        document.getElementById('itemList').innerHTML = '';
        
        // Limpar o campo oculto
        document.getElementById('regioes_input').value = '';
    });

    // Event listener para o formulário
    document.getElementById('inserirEntregaForm').addEventListener('submit', async function(event) {
        event.preventDefault();

        const motorista = document.getElementById('motorista').value;
        const placa = document.getElementById('placa').value;
        const regioes = document.getElementById('regioes_input').value;
        const kmInicial = document.getElementById('km_inicial').value;
        const numNotas = document.getElementById('num_notas').value;
        const numeroEntrega = document.getElementById('numero_entrega').value;
        const veiculo = document.getElementById('veiculo').value;

        try {
            const response = await fetch('/inserir_entrega', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    numero_entrega: numeroEntrega,
                    motorista,
                    placa,
                    veiculo,
                    km_inicial: kmInicial,
                    num_notas: numNotas,
                    regioes
                })
            });

            if (response.ok) {
                console.log('Entrega inserida com sucesso');
                // Redirecionar para o dashboard
                window.location.href = '/dashboard';  // Redireciona para a rota do dashboard
            } else {
                console.error('Erro ao inserir entrega:', response.statusText);
            }

        } catch (error) {
            console.error('Erro ao enviar o formulário:', error);
        }
    });
});