#arquivo diferente 
import random

def obter_mensagem_por_nota(nota: float) -> str:


    mensagens = {
        0: [
            "Não desanime! Todo começo é um passo importante.",
            "Errar faz parte do aprendizado. Recomece com calma.",
            "Cada tentativa é uma oportunidade de aprender algo novo.",
            "Use essa nota como motivação para se dedicar mais.",
            "Todo mundo começa do zero. Você só precisa continuar.",
            "Você é capaz! Recomece e verá resultados.",
            "Não se preocupe com o erro, preocupe-se em tentar de novo.",
            "O fracasso só é definitivo quando você desiste.",
            "Hoje é zero, mas amanhã pode ser dez!",
            "Grandes vitórias nascem das tentativas mais difíceis."
        ],
        1: [
            "Você deu o primeiro passo, e isso já é um progresso!",
            "Pequenos avanços levam a grandes conquistas.",
            "Continue estudando, você está no caminho.",
            "Com prática e paciência, a melhora vem rápido.",
            "Aprender leva tempo — siga firme!",
            "Reveja os conceitos básicos, isso vai te ajudar muito.",
            "Cada erro é uma chance de crescer.",
            "Não desista, sua evolução já começou.",
            "Você pode transformar essa nota em algo incrível.",
            "Errar é parte essencial do aprendizado!"
        ],
        2: [
            "Você já entendeu parte do conteúdo, continue assim!",
            "Um pouco mais de foco e você vai longe.",
            "Reforce o que aprendeu, e o resultado virá.",
            "Praticar é a chave para melhorar.",
            "Você está construindo uma boa base.",
            "Cada estudo é um passo para a nota máxima.",
            "Foque nas partes que mais tem dificuldade.",
            "Revise com calma, sem pressa.",
            "Você está progredindo, mesmo que pareça pouco.",
            "Continue acreditando em si mesmo!"
        ],
        3: [
            "Bom esforço! Falta pouco para atingir a média.",
            "Você já tem o básico, agora é fortalecer o resto.",
            "Continue praticando, os resultados virão.",
            "Você está aprendendo, continue firme!",
            "Cada dia estudando é um passo adiante.",
            "Não pare agora, está quase lá!",
            "Revise os temas em que teve mais dificuldade.",
            "Você está melhorando, continue assim.",
            "Foco, paciência e persistência — você chega lá.",
            "Sua dedicação faz toda a diferença!"
        ],
        4: [
            "Está quase na metade do caminho, parabéns!",
            "Você está evoluindo, continue estudando.",
            "Um pequeno esforço a mais pode te colocar na média.",
            "Reforce os temas mais desafiadores.",
            "Sua nota mostra que o aprendizado está vindo.",
            "Continue tentando, o progresso é visível.",
            "Aproveite os erros para aprender mais.",
            "Você está indo muito bem, falta pouco!",
            "Continue revisando, logo chegará ao 7.",
            "Seu esforço está valendo a pena!"
        ],
        5: [
            "Boa! Você está na média, mas pode ir além!",
            "Continue se dedicando, o 7 está logo ali.",
            "Revise os pontos que ainda geram dúvida.",
            "Você tem potencial para subir ainda mais!",
            "A constância nos estudos vai te levar ao sucesso.",
            "Reforce seu aprendizado com exercícios práticos.",
            "Continue estudando, sua base está sólida.",
            "Você está crescendo, continue nesse ritmo.",
            "A média é um bom sinal, mas o melhor está por vir.",
            "Você está construindo um ótimo caminho!"
        ],
        6: [
            "Muito bom! Sua nota mostra um bom domínio.",
            "Continue assim e logo chegará ao topo.",
            "Revise o que errou para consolidar o aprendizado.",
            "Você está indo muito bem, parabéns!",
            "Aproveite o ritmo e siga evoluindo.",
            "Você está acima da média, mantenha o foco.",
            "Pequenos detalhes farão você alcançar o 10.",
            "Excelente progresso, continue estudando.",
            "Sua dedicação está dando frutos!",
            "Falta pouco para a excelência!"
        ],
        7: [
            "Parabéns! Você está acima da média.",
            "Seu desempenho é ótimo, continue assim!",
            "Você está no caminho certo para o sucesso.",
            "Aproveite para revisar e fixar o conteúdo.",
            "Um pouco mais de prática e você alcança o 10!",
            "Continue com esse ritmo, está excelente!",
            "Seu esforço está refletindo nos resultados.",
            "Muito bem! Mantenha a constância.",
            "Essa nota mostra que você está aprendendo de verdade.",
            "Você está indo muito bem, parabéns!"
        ],
        8: [
            "Excelente! Falta pouco para a nota máxima.",
            "Continue estudando, o 10 está logo ali!",
            "Você está com ótimo domínio do conteúdo.",
            "Seu desempenho é excelente!",
            "Continue praticando para alcançar a perfeição.",
            "Você está no caminho certo, mantenha o foco!",
            "Muito bom! Continue nesse ritmo.",
            "Parabéns! Sua dedicação é inspiradora.",
            "Você mostrou um ótimo entendimento do tema.",
            "Brilhante trabalho, continue assim!"
        ],
        9: [
            "Uau! Quase perfeito, parabéns!",
            "Você está entre os melhores!",
            "Excelente desempenho, continue evoluindo.",
            "Falta pouco para o 10, você consegue!",
            "Continue revisando para manter o nível.",
            "Você domina o conteúdo, parabéns!",
            "Seu esforço é admirável!",
            "Essa nota mostra seu comprometimento.",
            "Você está quase lá, continue brilhando!",
            "Fantástico resultado, mantenha o foco!"
        ],
        10: [
            "Perfeito! Você é um exemplo de dedicação!",
            "Parabéns, excelência total!",
            "Seu esforço e foco trouxeram o sucesso!",
            "Você atingiu o máximo, incrível!",
            "Continue assim e inspire outros colegas!",
            "Brilhante! Seu desempenho é admirável.",
            "Você dominou o conteúdo por completo!",
            "Nota máxima merecida, parabéns!",
            "Continue mantendo esse padrão de excelência!",
            "Você mostrou o que é dedicação e empenho!"
        ]
    }

    nota_int = int(round(nota))
    nota_int = max(0, min(10, nota_int))  
    return random.choice(mensagens[nota_int])
