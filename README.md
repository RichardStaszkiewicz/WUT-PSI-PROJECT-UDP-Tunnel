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
|  Send to IP          | Tunel Server-End IP   | Web Server IP          |
|  Send to Port        | Tunel Server-End Port | Web Server Port        |
|  Response to IP      | _Not applicable_      | Tunel Client-End IP    |
|  Response to Port    | _Not applicable_      | Tunel Client-End Port  |
|  TCP Port            | Opened TCP Port No.   | Opened TCP Port No.    |
|  TCP Buffer Size     | TCP Buffer Size       | TCP Buffer Size        |
|  TCP Backlog         | Amount of backloged c.| _Not applicable_       |
|  TCP is listen       | **CONST 1**           | **CONST 0**            |
