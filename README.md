# Εξερευνητής (Exereunetes)

Z greckiego "odkrywca". Program realizujący takie
zadania jak dodawanie funkcji lub generowanie
dokumentacji dla ZUPEŁNIE NIEZNANEGO systemu do którego
kodu mamy dostęp. W ramach narzędzia istnieją
funkcjonalności `chat` i `apply`.

Funkcjonalność `chat` potrafi:
- Dodawać funkcje do już istniejącego kodu
- Generować dokumentację
- Odpowiadać na pytania dotyczące systemu

Funkcjonalność `apply` potrafi:
- Zastosować zmiany do projektu na podstawie instrukcji
wygenerowanej przez `chat`

**UWAGA:** Obecnie działa jedynie funkcjonalność `chat`,
`apply` nie działa.

# Jak używać programu
Działanie programu jest w pełni autonomiczne. Jedyne
co musimy mu przekazać to ścieżka do katalogu z projektem,
nazwa projektu i którtki opis projektu. W opisie projektu
nie musimy wchodzić w żadne szczegóły techniczne. Te parametry
ustawiamy w zmiennych `project_name` i `basic_message` w
pliku `cmd_chat.py`.

Domyślnie program jest skonfigurowany pod projekt
Django-School-Management-System. Ścieżka do repozytorium
tego projektu jest ustawiona jako `./Django-School-Management-System/`.

Żeby móc użyć programu w obecnej konfiguracji trzeba do katalogu
głównego projektu Εξερευνητής sklonować repozytorium
Django-School-Management-System.

```
git clone https://github.com/adigunsherif/Django-School-Management-System.git
```

Trzeba też dostarczyć klucz OpenAI API. Należy go umieścić
w pliku `api_key.txt`.

Po zrobieniu tego będzie możliwe używanie skryptu
`./exereunetes.py`, który jest prostym CLI dla naszego
rozwiązania.

# Przykłady

Prośba o dodanie funkcjonalności
```
exereunetes chat "Add footer with aurhors information to the webpage."
```

Program **exeraunetes** odpowie dokładną instrukcją,
w której będzie wytłumaczone jak dodać stopkę z
informacjami o autorach do strony internetowej
systemu Django-School-Management-System.

Następnie można postępując według instrukcji dodać
taką funkcjonalność do systemu, albo użyć komendy do
automatycznego jej dodania. Żeby tak zrobić trzeba
utworzyć plik z opisem funkcjonalności i wklejić
do niego rozwiązanie zaproponowane przez
**exeraunetes chat** i wywołać komendę **exeraunetes apply**.
```
exereunetes apply my_feature_description.txt
```
