document.addEventListener('DOMContentLoaded', () => {
    async function carregarSugestoes(url, elementoId) {
        try {
            const response = await fetch(url);
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

    // Carregar sugestões de motoristas
    carregarSugestoes('/sugestoes_motoristas', 'motorista');

    // Event listener para o primeiro formulário (Relatório de KM Rodados)
    document.getElementById('relatorioConsumoCombustivelForm').addEventListener('submit', async function(event) {
        event.preventDefault();

        const motorista = document.getElementById('motorista').value;
        const dataInicial = document.getElementById('dataInicial').value;
        const dataFinal = document.getElementById('dataFinal').value;

        try {
            const response = await fetch('/consumo_combustivel', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    motorista,
                    dataInicial,
                    dataFinal
                })
            });

            const data = await response.json();
            const resultados = data.resultados;
            const total_entregas = data.total_entregas;

            // Limpar a tabela antes de preencher com novos dados
            const tabelaBody = document.querySelector('#resultado tbody');
            tabelaBody.innerHTML = '';

            // Preencher a tabela com os resultados
            resultados.forEach(resultado => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${resultado[0]}</td> <!-- Motorista -->
                    <td>${resultado[1]}</td> <!-- Placa -->                    
                    <td>${resultado[2]}</td> <!-- Veiculo -->  
                    <td>${resultado[3]}</td> <!-- Total KM -->  
                    <td>${resultado[4]}</td> <!-- Total Litros -->  
                    <td>${resultado[5]}</td> <!-- Consumo KM/L -->  
                `;
                tabelaBody.appendChild(row);
            });

        } catch (error) {
            console.error('Erro ao gerar o relatório:', error);
        }
    });
});