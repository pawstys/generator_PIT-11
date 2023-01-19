# generator_PIT-11
Program do generowania deklaracji PIT-11 w postaci plików xml na podstawie danych w plikach csv. Dane wejściowe należy wprowadzić w plikach: firma.csv
(dane podmiotu wystawiającego deklaracje PIT-11 - jeden wiersz) oraz dane.csv (dane osób fizycznych, dla których zostaną wystawione deklaracje - dla każdej
z osób w osobnym wierszu). Plik dane.csv zawiera minimalną ilość kolumn, których wypełnienie pozwala na prawidłowe wypełnienie deklaracji.
W przypadku brakujących kolumn (np. od P_34 do P_120) można je uzupełnić w tym pliku.
Pliki wynikowe zostaną zapisane w katalogu PIT-11. Po wygenerowaniu pliku program dokonuje sprawdzenia zgodności wygenerowanej deklaracji ze schemą xsd
pobraną ze strony Ministerstwa Finansów: https://www.podatki.gov.pl/e-deklaracje/dokumentacja-it/struktury-dokumentow-xml a następnie zwraca informację zwrotną.
Poprawnie wygenerowane pliki można wczytać do formularza interaktywnego PDF pobranego ze strony MF za pomocą opcji Edycja -> Opcje formularza -> Importuj dane
(plik PDF znajduje się w katalogu głównym programu). Program nie obsługuje załączników PIT-R (przyjmuje, że informacja nie jest dołączona).
