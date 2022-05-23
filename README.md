2. Interpretacja
Aktor:
 -> Klient dummy wysyłający TCP na port X do samego siebie
 -> Klient: Otrzymuje połączenie TCP na port X i przesyła z pomocą UDP na port Y serwera
 -> Serwer: Otrzymuje wiadomości UDP i tworzy połączenie TCP do Internetu

Datagram:
-> Z chroma łączymy się na 127.0.0.1:X
-> Klient (Router) dostaje TCP o Src: 127.0.0.1, Dest: 127.0.0.1:X
-> Klient (Router) wysyła UDP z informacjami połączenia na Serwer hardcoded Dest
-> Serwer (Router) dostaje UDP z informacjami o TCP i nawiązuje sesję z hardcoded Dest

3. Piszesz do przeglądarki 127.0.0.1:2000 i otwiera się google.com (Magic)
4. Protokoły komunikacjyjne TCP i UDP
5. Moduł klient i moduł serwer
6. zrobiona implementacja podstawowa

1, 2 -> Client
3, 4 -> Server

# Config file

## TL;DR
Config file is in .json format and specifies a host tunnel end.

## Structure
|  Tag                 | Client Description    | Server Description     |
|:--------------------:|:---------------------:|:----------------------:|
|  Host IP             | Host IP to bind sock  | Host IP to bind sock   |
|  Send UDP to IP      | Tunel Server-End IP   | Tunel Client-End IP    |
|  Send UDP to Port    | Tunel Server-End Port | Tunel Client-End Port  |
|  Send TCP to IP      | _Not applicable_      | Web Server IP          |
|  Send TCP to Port    | _Not applicable_      | Web Server Port        |
|  UDP Client Port     | Client UDP Port No.   | Client UDP Port No.    |
|  UDP Server Port     | Server UDP Port No.   | _Not applicable_       |
|  TCP Port            | Opened TCP Port No.   | Opened TCP Port No.    |
|  TCP Buffer Size     | TCP Buffer Size       | TCP Buffer Size        |
|  UDP Buffer Size     | UDP Buffer Size       | UDP Buffer Size        |
|  TCP Backlog         | Amount of backloged c.| _Not applicable_       |
|  TCP is listen       | **CONST 1**           | **CONST 0**            |
