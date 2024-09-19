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

    // Carregar sugestões de regioes
    carregarSugestoes('/sugestoes_regioes', 'regiao');

    // Event listener para o primeiro formulário (Relatório de KM Rodados)
    document.getElementById('relatorioEntregaRegiaoForm').addEventListener('submit', async function(event) {
        event.preventDefault();

        const regiao = document.getElementById('regiao').value;
        const dataInicial = document.getElementById('dataInicial').value;
        const dataFinal = document.getElementById('dataFinal').value;

        try {
            const response = await fetch('/entrega_regiao', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    regiao,
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
                    <td>${resultado[0]}</td> <!-- Região -->
                    <td>${resultado[1]}</td> <!-- Numero de Entregas -->                    
                `;
                tabelaBody.appendChild(row);
            });

            // Exibir o total de entregas
            const totalRow = document.createElement('tr');
            totalRow.innerHTML = `
                <td colspan="1"><strong>Total de Entregas:</strong></td>
                <td colspan="1"><strong>${total_entregas}</strong></td>
            `;
            tabelaBody.appendChild(totalRow);

        } catch (error) {
            console.error('Erro ao gerar o relatório:', error);
        }
    });
});