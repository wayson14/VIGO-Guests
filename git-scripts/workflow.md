1. Przed rozpoczęciem sesji pisania pullujemy branch *main* z remote - tak żebyśmy mieli tę samą wersję co jest na serwerze.
      ```shell
   git fetch 
   git merge origin/main
```
2. Piszemy normalnie kod, po zaimplementowaniu ważniejszych featurów commitujemy do naszej lokalnej wersji repo
      ```shell
   git add .
   git commit -m "Added delete button." 
	#zawsze trzeba dać wiadomość do commitu, o ile nie chcemy dostać ekranu vima na twarz
   ```
3. Kiedy kończymy pracę nad featurem i chcemy spushować nasze lokalne repo na remote (serwer github), najpierw musimy pobrać repo z serwera z jego aktualną wersją, która mogła się zmienić. Robimy to za pomocą komendy:
   ```shell
   git fetch #domyślnie z origin/main
```
4. Następnie, przenosimy nasz commit na sam przód historii za pomocą komendy.
   ```shell
	git rebase origin/main
	```
	- *Działanie rebase*
		https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase
	- *Działanie merge* (użyte na początku)
		https://www.atlassian.com/git/tutorials/using-branches/git-merge
5. Jeżeli na tym etapie pojawią się jakiekolwiek konflikty, rozwiązujemy je (instrukcja na końcu).
6. Kiedy pomyślnie udało nam się zrobić rebase, możemy pushować na githuba:
   ```shell
   git push -u origin main
```

