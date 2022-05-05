# VIGO-Guests
Usługa rejestrująca wejścia gości do siedziby firmy VIGO S.A.

### Struktura
Aplikacja składa się z następujących interfejsów:
- interfejs gościa umożliwiający podanie swoich danych osobowych
- interfejs recepcjonisty, dzięki któremu można zarejestrować wizytę
- panel administracyjny
- panel główny

### Wymagania systemowe
- postgresql
- python >= 3.8 oraz paczki podane w pliku **req.txt**
- redis-server
- daphne
- tmux*
  *przydatny, jeżeli chcemy korzystać z pełni możliwości automatyzacji

### Działanie
Gość podaje swoje dane w interfejsie gościa. Są odpowiednio przetwarzane i wysyłane na serwer za pomocą skryptu JS. Dane na serwerze są wstępnie zapisywane w bazie danych. Jednocześnie wysyłany jest event protokołem WebSockets, informujący o nowym wpisie. 

Interfejs recepcjonistki, który jest połączony na tym samym kanale WS odbiera event i pobiera dane z serwera dotyczące nowych wpisów. 
Recepcja może w tym momencie dodać kartę gościa do wpisu lub taki wpis odrzucić ze względu na niepoprawność wpisanych danych. W przypadku odrzucenia wpis jest usuwany z bazy danych. W przypadku zapisania z kartą jest odpowiednio modyfikowany.

Po zakończeniu wizyty, recepcja kończy wejście przyciskiem "zwolnij". W tym momencie dopisywana jest data wyjścia a karta pozostaje zwolniona i jest możliwa do pobrania przez następne wejście.

### Uruchamianie i przeładowywanie
Do działania aplikacji należy uruchomić skrypt *vigo-guests-full-reload-prod.sh* znajdujący się w folderze domowym usera sysadmin. 

W folderach *~/VIGO-Guests/django-scripts, git-scirpts* znajdują się skrypty automatyzujące proces aktualizowania i przeładowania aplikacji. Są one umieszczone w repozytorium projektu, ponieważ są specyficzne dla aplikacji. Skrypt */django-scripts/prod-full-start.sh* nie jest śledzony przez gita i jest on specyficzny dla środowiska. Można go łatwo odtworzyć modyfikując plik **template-prod-full-start.sh**.

### Kody dla różnych typów kart:
<100, 199> zwykły gość
<200, 299> pełny serwis
<700, 799> administrator