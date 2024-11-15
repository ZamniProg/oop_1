import requests
import webbrowser


class Color:
    Reset = '\033[0m'

    Red = '\033[91m'
    Green = '\033[92m'
    Yellow = '\033[93m'
    Black = '\033[94m'


class GetInput:
    def __init__(self):
        self.query = ""

    def get_user_input(self):
        while True:
            self.query = input('Введите запрос: ').strip()
            if len(self.query) == 0:
                print("{}[?]{} Неверный ввод! Повторите попытку еще раз!\n".format(Color.Yellow, Color.Reset))
            else:
                break

    @staticmethod
    def get_choice(results):
        while True:
            choice = input("Введите номер статьи для открытия ({} - {}) - ".format(1, len(results)))
            if choice.isdigit() and 0 < int(choice) <= len(results):
                return int(choice)
            print('{}[?]{} Введен неверный номер! Попробуйте еще раз!'.format(Color.Yellow, Color.Reset))

    @staticmethod
    def check_parse(data):
        if not data or 'query' not in data or len(data['query']['search']) == 0:
            print("{}[!]{} К сожалению по запросу ничего не было найдено".format(Color.Red, Color.Reset))
            return 0
        return 1


class WikiSearch(GetInput):
    def __init__(self):
        super().__init__()
        self.get_user_input()
        self.search_results = []

    def search(self):
        url = 'https://ru.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'list': 'search',
            'format': 'json',
            'srsearch': self.query
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            self.parse_result(data)
        except requests.RequestException as e:
            print("{}[!]{} Ошибка при выполнении запроса: {}".format(Color.Red, Color.Reset, e))

    def parse_result(self, data):
        if self.check_parse(data):
            self.search_results = data['query']['search']
            for i, result in enumerate(self.search_results, 1):
                title = result['title']
                snippet = result['snippet'].replace("<span class=\"searchmatch\">", "").replace('</span>', "")
                print('{}{} -> {}{}{}{}:\n\t {}'.format(Color.Green,
                                                        i,
                                                        Color.Reset,
                                                        Color.Black,
                                                        title,
                                                        Color.Reset,
                                                        snippet))

    def open_browser(self):
        if len(self.search_results):
            choice = self.get_choice(self.search_results)
            title = self.search_results[choice - 1]["title"]
            url = f'https://wikipedia.org/wiki/{title.replace(' ', '_')}'
            webbrowser.open(url)
            print('{}Идет открытие статьи: {}{} - {}'.format(Color.Green, Color.Reset, choice, title))


def main():
    search = WikiSearch()
    search.search()
    search.open_browser()


if __name__ == '__main__':
    main()
