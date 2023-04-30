from parcial2all import csv_parse


def test_csv_parse():
    info = [("Deportes", "Messi marca un gol histórico", "https://www.ejemplo.com/deportes/messi-gol-historico"),
            ("Política", "Candidato X presenta su plan de gobierno", "https://www.ejemplo.com/politica/candidato-x-plan-gobierno")]

    expected_output = "categoria, titulo, link\nDeportes, Messi marca un gol histórico, https://www.ejemplo.com/deportes/messi-gol-historico\nPolítica, Candidato X presenta su plan de gobierno, https://www.ejemplo.com/politica/candidato-x-plan-gobierno\n"

    assert csv_parse(info) == expected_output
