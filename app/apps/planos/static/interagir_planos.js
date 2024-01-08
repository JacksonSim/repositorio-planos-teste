function destacar(elementoClicado) {
    // Identificar o grupo do elemento clicado
    var grupo = elementoClicado.getAttribute('data-group');

    // Remover destaque de todos os elementos no mesmo grupo
    var elementosMesmoGrupo = document.querySelectorAll('.tipo_portifolio[data-group]');
    elementosMesmoGrupo.forEach(function (elemento) {
        elemento.classList.remove('destaque');
    });

    // Adicionar destaque ao elemento clicado
    elementoClicado.classList.add('destaque');

    // Mostrar apenas as divs com o mesmo valor do atributo data-tipo_portifolio
    var divsParaMostrar = document.querySelectorAll('.bloco_plano_completo[data-tipo_portifolio="' + grupo + '"]');
    divsParaMostrar.forEach(function (div) {
        div.classList.add('mostrar');
    });

    // Ocultar as demais divs
    var divsParaOcultar = document.querySelectorAll('.bloco_plano_completo:not([data-tipo_portifolio="' + grupo + '"])');
    divsParaOcultar.forEach(function (div) {
        div.classList.remove('mostrar');
    });
}

document.addEventListener('DOMContentLoaded', function () {
    var box_plan_id = 0;  // Variável para armazenar o ID do selectBox em foco

    // Adicione um evento de foco para cada selectBox
    var selectBoxes = document.querySelectorAll('.form-control.combobox');
    selectBoxes.forEach(function (selectBoxe) {
        selectBoxe.addEventListener('focus', function () {
            // Obtém o ID do selectBox em foco
            box_plan_id = this.id;
            console.log("ID do selectBox em foco:", box_plan_id);


            if (box_plan_id === 0) {
                console.log('nenhum valor');
            } else {
                // Obtendo o valor do atributo "data-acordo" da opção "Sem fidelidade"
                var selectBox = document.getElementById(box_plan_id);
                // Obtendo o ID do bloco
                // var box_plan_id = selectBox.getAttribute('id');
                var vlr_sem_fidelidade = Number(0);
                var vlr_com_fidelidade = Number(0);
                var vigencia = 0;
                var valor_economia = Number(0);

                // Obtendo o valor do atributo "data-acordo"
                var optionSemFidelidade = selectBox.querySelector('option[data-fid="0"]');
                vlr_sem_fidelidade = optionSemFidelidade.getAttribute('data-acordo');

                // Selecionando a div com a classe "valor_com_destaque"
                var valorComFidelidadeElement = document.querySelector('.valor_com_destaque[data-id="' + box_plan_id + '"] span');

                selectBox.addEventListener('change', function () {
                    // Obtendo a opção selecionada
                    var selectedOption = selectBox.options[selectBox.selectedIndex];

                    // Obtendo os atributos da opção selecionada
                    vlr_com_fidelidade = selectedOption.getAttribute('data-acordo');
                    vigencia = selectedOption.getAttribute('data-fid');

                    // Calculando o valor da economia
                    var vlr = vlr_com_fidelidade.toString().replace(',','.');
                    vlr_com_fidelidade = Number(vlr);
                    vlr = vlr_sem_fidelidade.toString().replace(',','.');
                    vlr_sem_fidelidade = Number(vlr);
                    
                    valor_economia = (vlr_sem_fidelidade * vigencia) - (vlr_com_fidelidade * vigencia);

                    valorComFidelidadeElement.textContent = parseFloat(vlr_com_fidelidade).toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

                    // Adicionando ou removendo as classes conforme a condição
                    var infAdicionaisElements = document.querySelectorAll('.inf_adicionais[data-id="' + box_plan_id + '"]');
                    infAdicionaisElements.forEach(function (element) {
                        if (vigencia === '0') {
                            element.classList.add('ocultar_bloco', 'reduzir_bloco');
                        } else {
                            element.classList.remove('ocultar_bloco', 'reduzir_bloco');
                        }
                    });

                    // Substituindo o texto em todas as instâncias da classe "inf_economize"
                    var infEconomize = document.querySelector('.inf_economize[data-id="' + box_plan_id + '"]');

                    infEconomize.innerHTML = `*<b>Economize R$ ${valor_economia.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</b> no final dos ${vigencia} Meses de Fidelidade.`;


                });

            }

        });
    });

    

});

function moedaBrasil(valor_economia){
    valor_economia.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function expandir(elementoClicado) {
    // Identificar o grupo do elemento clicado
    var grupo = elementoClicado.getAttribute('data-group');
}

document.getElementById('itensLista_Plan1').addEventListener('show.bs.collapse', function () {
    document.querySelector('.all_icon_itens_combo').classList.remove('show');
});

document.getElementById('itensLista_Plan1').addEventListener('hidden.bs.collapse', function () {
    document.querySelector('.all_icon_itens_combo').classList.add('show');
});