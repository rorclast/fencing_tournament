# fencing_tournament
A Python 3 solution to a fencing tournament problem (inside a Laravel 5 project)

The problem description is found in the file FencingTournament.pdf and it's solution
in FencingTournament.py. There's also an artisan command to generate test cases for
the problem. To create a test case:

  (1) clone the repo,
  (2) install composer (if it's not installed),
  (3) navigate to the repo's root directory,
  (4) execute the command 'composer install' on the command line,
  (5) execute 'cp .env.local .env',
  (6) execute 'mkdir storage/app/tournament', and
  (7) execute 'php artisan tournament:generate [number_of_rows_you_want]'.
  
The test cases are stored in the storage/app/tournament directory.
