// Aguarda o documento HTML carregar completamente antes de rodar o JS
document.addEventListener("DOMContentLoaded", function() {
    
    // Seleciona todos os links que tenham a classe 'btn-deletar'
    const botoesDeletar = document.querySelectorAll(".btn-deletar");

    botoesDeletar.forEach(botao => {
        botao.addEventListener("click", function(event) {
            // Cria um alerta de confirmação nativo
            const confirmacao = confirm("Atenção: Tem certeza que deseja apagar este item?");
            
            // Se o usuário clicar em "Cancelar", o JS impede que o link redirecione para a rota do Flask
            if (!confirmacao) {
                event.preventDefault();
            }
        });
    });
});