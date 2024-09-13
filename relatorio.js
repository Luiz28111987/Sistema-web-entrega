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

    carregarSugestoes('/sugestoes_motoristas', 'motorista');

    const form = document.getElementById('relatorioForm');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const motorista = document.getElementById('motorista').value;
        const dataInicial = document.getElementById('dataInicial').value;
        const dataFinal = document.getElementById('dataFinal').value;

        try {
            const response = await fetch('/consulta_relatorio', {
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
            const totalKm = data.total_km;

            // Limpar a tabela antes de preencher com novos dados
            const tabelaBody = document.querySelector('#resultado tbody');
            tabelaBody.innerHTML = '';

            // Preencher a tabela com os resultados
            resultados.forEach(resultado => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${resultado[0]}</td> <!-- Motorista -->
                    <td>${resultado[4]}</td> <!-- Veículo -->
                    <td>${resultado[1]}</td> <!-- Placa -->
                    <td>${resultado[5]}</td> <!-- KM Rodado -->
                    <td>${resultado[6]}</td> <!-- Notas Transportadas -->
                    <td>${resultado[7]}</td> <!-- Notas Coletadas -->
                    <td>${resultado[2]}</td> <!-- Regiões -->
                `;
                tabelaBody.appendChild(row);
            });

            // Exibir o total de KM Rodado
            const totalRow = document.createElement('tr');
            totalRow.innerHTML = `
                <td colspan="3"><strong>Total de KM Rodado:</strong></td>
                <td colspan="4"><strong>${totalKm}</strong></td>
            `;
            tabelaBody.appendChild(totalRow);

        } catch (error) {
            console.error('Erro ao gerar o relatório:', error);
        }
    });
});