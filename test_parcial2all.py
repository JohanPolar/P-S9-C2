from parcial2all import csv_parse

def test_csv_parse():
        info = [
            ('category1', 'title1', 'link1'),
            ('category2', 'title2', 'link2'),
            ('category3', 'title3', 'link3')
        ]

        csv_result = csv_parse(info)

        expected_csv = "categoria, titulo, link\n" \
                       "category1, title1, link1\n" \
                       "category2, title2, link2\n" \
                       "category3, title3, link3\n"
        assert csv_result == expected_csv
