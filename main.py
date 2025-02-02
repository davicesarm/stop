import random
import string
import curses

def is_stop_valid(answers: dict[str, str], letter: str) -> bool:
    for value in answers.values():
        if not value.lower().startswith(letter.lower()):
            return False
    return True

def jogo(stdscr: curses.window) -> None:
    categorias = [
        "Nome", "Cidade", "Animal", "Objeto", "Cor", "Fruta",
        "Profissão", "Time de Futebol", "País", "Filme"
    ]
    letra = random.choice(string.ascii_uppercase)
    respostas = {categoria: "" for categoria in categorias}
    
    selecionado = 0
    stdscr.clear()
    stdscr.refresh()
    
    while True:
        curses.curs_set(0)
        stdscr.clear()
        stdscr.addstr(0, 0, "Use ↑ e ↓ para selecionar, Enter para editar, F para STOP\n")
        stdscr.addstr(1, 0, f"A LETRA SORTEADA É: {letra}\n")
        
        for i, categoria in enumerate(categorias):
            if i == selecionado:
                stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(i + 3, 0, f"{categoria}: {respostas[categoria]}")
            if i == selecionado:
                stdscr.attroff(curses.A_REVERSE)
        
        key = stdscr.getch()
        
        if key == curses.KEY_UP:
            selecionado = (selecionado - 1) % len(categorias)
        elif key == curses.KEY_DOWN:
            selecionado = (selecionado + 1) % len(categorias)
        elif key == ord('f'):
            if is_stop_valid(respostas, letra):
                break
            else:
                stdscr.addstr(len(categorias) + 4, 0, "STOP inválido!")
                stdscr.refresh()
                stdscr.getch()
        elif key == 10:  # Enter
            digite = "Digite a palavra (enter para voltar): "
            stdscr.addstr(len(categorias) + 4, 0, digite)
            stdscr.refresh()
            curses.echo()
            curses.curs_set(1)
            resposta: str = stdscr.getstr(len(categorias) + 4, len(digite), 20).decode("utf-8").strip()
            curses.noecho()
            if resposta != "":
                respostas[categorias[selecionado]] = resposta
    
    stdscr.clear()
    stdscr.addstr(0, 0, "Resultados:\n")
    for i, (categoria, resposta) in enumerate(respostas.items()):
        stdscr.addstr(i + 1, 0, f"{categoria}: {resposta}")
    stdscr.addstr(len(categorias) + 1, 0, "\nFim da rodada! Pressione qualquer tecla para sair.")
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(jogo)
